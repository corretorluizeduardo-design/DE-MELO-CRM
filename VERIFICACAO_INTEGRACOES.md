# Verificação das integrações preservadas

A edição De Melo foi preparada a partir do arquivo completo `DeskcommCRM-main.zip`. O pacote inclui o código e os módulos de instalação originais, com ajustes de marca e configuração de repositório.

Foram comparados **215 arquivos** contra a árvore extraída original, por SHA-256, nas áreas abaixo. Todos os hashes coincidiram durante a preparação:

- `lib/waha/`
- `lib/channels/`, incluindo `lib/channels/meta/`
- `app/api/v1/channels/` e `app/api/v1/webhooks/`, incluindo o webhook Meta e WAHA
- onboarding, telas de Conexões, sessões de canal e roteamento
- envio de mensagens da IA e envio de fotos do catálogo
- endpoints de mídia das conversas e das mensagens

Para conferir novamente a partir da raiz do repositório:

```bash
sha256sum -c WHATSAPP_INTEGRACOES_SHA256SUMS.txt
```

O configurador `scripts/configurar_repo_demelo.py` altera endereços de repositório, namespace de imagens, documentação de instalação e o nome/cor da marca. Ele não reescreve o conteúdo dos conectores WAHA/Meta nem os endpoints acima.

## Limite funcional importante

O código original do catálogo já permite até cinco fotos JPG/PNG e o agente pode enviá-las ao cliente quando usa o código do item. A versão completa aqui não adiciona ainda campos próprios de upload de vídeo e link do Google Maps por empreendimento; essa extensão de banco, tela e fluxo de IA precisa ser implementada e testada separadamente. A prévia HTML anterior não substitui esses serviços reais.
