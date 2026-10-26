#!/usr/bin/env python3
"""Configura a cópia DE MELO CRM para seu repositório GitHub/GHCR próprio.

Uso: python scripts/configurar_repo_demelo.py --owner SEU_USUARIO --repo DE-MELO-CRM
Executar antes do primeiro push; não toca nos conectores WhatsApp.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = "https://github.com/melgarafael/DeskcommCRM"
UPSTREAM_GIT = UPSTREAM + ".git"


def write_replace(rel: str, replacements: list[tuple[str, str]], required: bool = True) -> int:
    path = ROOT / rel
    if not path.exists():
        if required:
            raise SystemExit(f"Arquivo necessário ausente: {rel}")
        return 0
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
    return int(text != original)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--owner", required=True, help="usuário/organização do GitHub")
    ap.add_argument("--repo", required=True, help="slug do repositório, ex.: DE-MELO-CRM")
    args = ap.parse_args()
    owner = args.owner.strip()
    repo = args.repo.strip()
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", owner):
        ap.error("--owner deve ser um nome simples de usuário/organização do GitHub")
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9._-]{0,98}[A-Za-z0-9])?", repo):
        ap.error("--repo deve ser um slug de repositório do GitHub")
    owner_lc = owner.lower()
    repo_url = f"https://github.com/{owner_lc}/{repo}"
    repo_git = repo_url + ".git"
    ns = f"ghcr.io/{owner_lc}"
    if (ROOT / ".git").exists():
        remote = __import__("subprocess").run(["git", "remote", "get-url", "origin"], cwd=ROOT,
                    text=True, capture_output=True)
        if remote.returncode == 0 and remote.stdout.strip() not in (repo_git, repo_url):
            print("AVISO: há um remote origin diferente; este script só configura URLs do código, não muda o remote.")
    changed = []

    # Descobre a identidade atual para permitir executar o configurador de novo
    # se o slug do repo mudar. NOTICE-DE-MELO.md preserva a URL upstream original.
    common_path = ROOT / "hostgator-setup-kit/_common.sh"
    common_text = common_path.read_text(encoding="utf-8")
    m_ns = re.search(r'^IMG_NS="([^"]+)"$', common_text, re.M)
    old_ns = m_ns.group(1) if m_ns else "ghcr.io/melgarafael"
    ident_path = ROOT / "tests/unit/_identidade-deste-repo.ts"
    ident_text = ident_path.read_text(encoding="utf-8")
    m_owner = re.search(r'export const NAMESPACE_DESTE_REPO = "ghcr.io/([^"]+)";', ident_text)
    m_repo = re.search(r'export const NOME_REPO_DESTE_REPO = "([^"]+)";', ident_text)
    old_owner = m_owner.group(1) if m_owner else old_ns.rsplit("/", 1)[-1]
    old_repo = m_repo.group(1) if m_repo else "DeskcommCRM"
    old_repo_url = f"https://github.com/{old_owner}/{old_repo}"
    old_repo_git = old_repo_url + ".git"
    old_raw = f"https://raw.githubusercontent.com/{old_owner}/{old_repo}"
    excluded = {"NOTICE-DE-MELO.md", "LICENSE", "CHANGELOG.md", "configurar_repo_demelo.py"}
    search_ext = {".md", ".sh", ".yml", ".yaml", ".ts", ".tsx", ".js", ".mjs", ".json", ".jsonc", ".txt", ".toml", ".py", ".env", ".example", ".dockerignore", ".gitignore", ".conf"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.name in excluded or ".git" in path.parts:
            continue
        if path.as_posix().endswith("docs/runbooks/remediar-worker-congelado.md"):
            continue  # documento histórico que registra o label de origem no upstream
        if any(part in {"node_modules", ".next", "coverage", "test-results", "evidence"} for part in path.parts):
            continue
        # The repo has some binary assets/fonts; only read known textual extensions.
        if path.suffix not in search_ext and path.name not in {"Dockerfile", "Dockerfile.worker", "Dockerfile.scheduler", "Dockerfile.voice-agent", "Caddyfile", "Caddyfile.single-server"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        original = text
        # Troca referências do upstream E da última identidade já configurada.
        # As duas formas de URL precisam ser migradas; os labels GHCR não derivam
        # de URLs, por isso o namespace é tratado explicitamente abaixo.
        text = text.replace(old_repo_git, repo_git).replace(old_repo_url, repo_url)
        text = text.replace(UPSTREAM_GIT, repo_git).replace(UPSTREAM, repo_url)
        # raw.githubusercontent links to install/update helper scripts also belong to this fork.
        text = text.replace(old_raw, f"https://raw.githubusercontent.com/{owner_lc}/{repo}")
        text = text.replace("https://raw.githubusercontent.com/melgarafael/DeskcommCRM", f"https://raw.githubusercontent.com/{owner_lc}/{repo}")
        # Os defaults de Compose/.env também precisam mudar, senão o runtime ainda
        # puxaria as imagens do dono antigo mesmo com o instalador configurado.
        text = text.replace(old_ns, ns)
        if path.as_posix().endswith("tests/unit/_identidade-deste-repo.ts"):
            text = re.sub(r'export const NAMESPACE_DESTE_REPO = "[^"]+";', f'export const NAMESPACE_DESTE_REPO = "{ns}";', text, count=1)
            text = re.sub(r'export const NOME_REPO_DESTE_REPO = "[^"]+";', f'export const NOME_REPO_DESTE_REPO = "{repo}";', text, count=1)
        if path.as_posix().endswith("hostgator-setup-kit/_common.sh"):
            text = re.sub(r'^IMG_NS="[^"]+"$', f'IMG_NS="{ns}"', text, count=1, flags=re.M)
        if path != (ROOT / "NOTICE-DE-MELO.md") and original != text:
            path.write_text(text, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))

    # Explicitly keep defaults consistent even if upstream changes formatting.
    required_literals = [
        ("hostgator-setup-kit/_common.sh", f'IMG_NS="{ns}"'),
        ("hostgator-setup-kit/install.sh", f'REPO_URL="${{REPO_URL:-{repo_git}}}"'),
        ("hostgator-setup-kit/comecar.sh", f'REPO_URL="${{REPO_URL:-{repo_git}}}"'),
        ("tests/unit/_identidade-deste-repo.ts", f'export const NAMESPACE_DESTE_REPO = "{ns}";'),
        ("tests/unit/_identidade-deste-repo.ts", f'export const NOME_REPO_DESTE_REPO = "{repo}";'),
        ("docker-compose.prod.yml", f"ghcr.io/{owner_lc}/deskcommcrm:stable"),
        (".env.hostgator.example", f"APP_IMAGE=ghcr.io/{owner_lc}/deskcommcrm:stable"),
    ]
    for rel, lit in required_literals:
        if lit not in (ROOT / rel).read_text(encoding="utf-8"):
            print(f"ERRO: configuração inconsistente em {rel}: esperado {lit}", file=sys.stderr)
            return 2

    print("Configuração aplicada.")
    print(f"Repositório: {repo_url}")
    print(f"Namespace de imagens: {ns}")
    print(f"Arquivos atualizados: {len(set(changed))}")
    print("Nenhum código de conector WhatsApp/WAHA/Meta foi substituído por implementação simulada.")
    print("Próximo passo: conferir git diff; depois inicializar git e publicar no GitHub.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
