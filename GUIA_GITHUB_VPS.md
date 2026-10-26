# DE MELO CRM — publicar no GitHub e instalar na VPS

Este pacote já foi configurado para o repositório informado:

- GitHub: https://github.com/corretorluizeduardo-design/DE-MELO-CRM
- Git remoto (HTTPS): https://github.com/corretorluizeduardo-design/DE-MELO-CRM.git
- Imagens Docker previstas: `ghcr.io/corretorluizeduardo-design/deskcommcrm`, `deskcomm-worker`, `deskcomm-scheduler` e `deskcomm-voice-agent`.

## 1. Publicar pelo Windows (PowerShell)

1. Baixe e extraia o ZIP do DE MELO CRM para uma pasta local. Use a pasta que contém `package.json`, `pnpm-lock.yaml`, `.github`, `app`, `lib` e `hostgator-setup-kit`.
2. Abra essa pasta no Explorador de Arquivos.
3. Clique na barra de endereço, digite `powershell` e pressione Enter.
4. Confira que está na raiz do repositório:

```powershell
Get-ChildItem package.json, pnpm-lock.yaml, hostgator-setup-kit\install.sh
```

5. Execute os comandos abaixo. O repositório GitHub foi criado vazio, portanto não é necessário dar `git pull` antes.

```powershell
git init -b main
git add .
git status --short
git commit -m "feat: DE MELO CRM baseado no DeskcommCRM"
git remote add origin https://github.com/corretorluizeduardo-design/DE-MELO-CRM.git
git push -u origin main
```

Se `git init -b main` não for aceito pela sua versão do Git, use `git init` e depois `git branch -M main` antes de adicionar/commit. Se pedir autenticação, conclua pelo navegador/Git Credential Manager; não coloque senha ou token em comandos.

Se o comando `git remote add origin` disser que `origin` já existe, use:

```powershell
git remote set-url origin https://github.com/corretorluizeduardo-design/DE-MELO-CRM.git
git push -u origin main
```

## 2. Esperar e validar a publicação das imagens

Depois do `git push`, abra o repositório e selecione **Actions**. Aguarde os workflows de validação/build. Para instalar o sistema, é necessário que as imagens `deskcommcrm`, `deskcomm-worker` e `deskcomm-scheduler` — e `deskcomm-voice-agent`, se usar voz — tenham sido publicadas no GitHub Container Registry (GHCR).

Se um workflow falhar, abra-o, leia o primeiro erro real e corrija-o antes de instalar. Não considere o sistema pronto só porque o código apareceu no GitHub.

Os pacotes GHCR precisam estar acessíveis à VPS. Se forem privados, configure autenticação de leitura na VPS antes da instalação; não publique chaves ou tokens no repositório. Para simplificar uma primeira instalação, pode tornar os pacotes publicados públicos nas configurações de cada pacote, se isso for adequado à sua operação.

## 3. Preparar a VPS

Antes de instalar, tenha:

- Ubuntu/Debian VPS com acesso SSH e Docker disponível (o kit trata a instalação do Docker quando aplicável);
- domínio com registro DNS `A` apontando para o IP da VPS;
- credenciais do Supabase ou acesso para criar/configurar o banco;
- chave de um provedor de IA (OpenAI, Anthropic ou OpenRouter);
- acesso ao WhatsApp que será conectado por QR/WAHA ou credenciais da Meta Cloud API para o canal oficial.

Não envie senhas, chaves de API ou tokens para o chat ou para arquivos versionados no GitHub.

## 4. Instalar na VPS

Conecte-se por SSH, substituindo o IP pelo endereço da sua VPS:

```bash
ssh root@SEU_IP
```

Depois, clone o repositório e execute o instalador oficial do kit incluído no projeto:

```bash
git clone https://github.com/corretorluizeduardo-design/DE-MELO-CRM.git
cd DE-MELO-CRM
bash hostgator-setup-kit/install.sh
```

Responda às perguntas do instalador com o domínio, dados do administrador, banco e provedor de IA. Confirme que ele está usando as imagens publicadas no namespace `ghcr.io/corretorluizeduardo-design`. Não prossiga caso ele informe que as imagens não existem ou não podem ser baixadas.

## 5. Depois da instalação

1. Acesse o domínio HTTPS e entre com o administrador criado.
2. Abra **Conexões** e configure o WhatsApp por QR/WAHA ou pela API oficial da Meta. Faça um teste de entrada e saída com uma conversa de teste.
3. Teste agentes de IA, recebimento de mensagens, mídia, tarefas, automações e avisos.
4. Execute o diagnóstico conforme a documentação do projeto: `bash hostgator-setup-kit/healthcheck.sh`.
5. Configure e valide backup regular antes de atender clientes reais.

## O que foi preservado e o que precisa ser validado

O projeto mantém os conectores, rotas e lógica originais do Deskcomm para WAHA/QR, Meta Cloud API, canais, mensagens, mídia, webhooks, banco, workers e agentes. A personalização de identidade não substitui esses conectores por simulações. A comparação de hashes realizada antes da publicação cobriu 215 arquivos selecionados dessas áreas e os encontrou idênticos ao pacote de origem.

A publicação e o build de produção ainda precisam ser executados no seu GitHub. Depois, a instalação e os testes de ponta a ponta precisam ser concluídos na sua VPS. Não considere os conectores operacionais até validar uma conexão real, recebimento e envio de mensagens.

## Segurança

- Não versionar `.env`, chaves privadas, tokens, backups ou sessões reais do WhatsApp.
- Usar MFA na conta GitHub e restringir quem pode publicar imagens/alterar workflows.
- Fazer backup antes de atualizações e antes de testar migrações no banco de produção.
- Seguir `SECURITY.md`, `hostgator-setup-kit/README.md` e `docs/SETUP.md` para requisitos e recuperação.
