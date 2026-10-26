# DE MELO CRM — aviso de origem e licença

Esta distribuição é uma edição personalizada do **DeskcommCRM**, projeto open source publicado por Rafael Melgar e colaboradores:

- Repositório de origem: https://github.com/melgarafael/DeskcommCRM
- Licença do código original: MIT (ver o arquivo `LICENSE` preservado neste pacote).
- As conexões e integrações de WhatsApp, agentes de IA, banco de dados, workers, testes e instalador VPS continuam baseadas no código-fonte original incluído integralmente nesta edição.

As personalizações desta edição incluem a marca DE MELO, logotipo próprio, padrão de nome/cor da instalação e o rótulo imobiliário do catálogo. A presença do código-fonte não significa que serviços externos (Meta, WAHA, Supabase, provedor de IA ou DNS) já estejam configurados: cada instalação precisa fornecer credenciais próprias e completar o onboarding.

Não publique chaves API, `.env`, tokens, backups com dados de clientes, credenciais SSH ou sessões de WhatsApp no GitHub. O `.gitignore` exclui os arquivos `.env*` com exceção dos templates seguros documentados no projeto.
