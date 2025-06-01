# 🤖 Bot Telegram - Sistema de Envio Automatizado

Sistema completo para envio automatizado de mensagens via Telegram com interface multilíngue, backup automático e relatórios detalhados.

## ✨ Funcionalidades

### 🔐 Segurança
- ✅ Autenticação obrigatória por senha
- ✅ Proteção contra múltiplos acessos
- ✅ Bloqueio temporário após tentativas incorretas

### 📊 Gestão de Planilhas
- ✅ Suporte a CSV e XLSX
- ✅ Validação automática de formato
- ✅ Processamento de colunas: `api_key`, `chat_id`, `mensagem`

### ⚙️ Configuração Flexível
- ✅ Intervalo personalizável entre envios
- ✅ Quantidade de mensagens por ciclo configurável
- ✅ Resumo visual antes de iniciar

### 🚀 Envio Inteligente
- ✅ Notificação em tempo real de cada envio
- ✅ Skip automático em caso de erro
- ✅ Controles de pausa/retomada
- ✅ Backup automático do progresso

### 🌍 Interface Multilíngue
- ✅ Português (PT-BR)
- ✅ Inglês (EN-US)
- ✅ Chinês Simplificado (ZH-CN)
- ✅ Detecção automática do idioma

### 📈 Relatórios
- ✅ Relatório final em CSV
- ✅ Status detalhado de cada envio
- ✅ Estatísticas de sucesso/erro

## 🛠️ Instalação

### 1. Clonar o repositório
```bash
git clone https://github.com/iovomia/botgerenciador.git
cd botgerenciador
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:
```env
BOT_TOKEN=seu_token_do_bot_telegram
SYSTEM_PASSWORD=kangoo@#2019
ADMIN_USER_ID=seu_id_telegram_opcional
```

### 4. Executar o bot
```bash
python main.py
```

## 📋 Como Usar

### 1. Iniciar o Bot
- Envie `/start` para o bot
- Digite a senha: `kangoo@#2019`

### 2. Enviar Planilha
- Envie arquivo CSV ou XLSX
- Formato obrigatório: `api_key`, `chat_id`, `mensagem`

### 3. Configurar Envio
- Defina intervalo entre envios (minutos)
- Defina quantidade de mensagens por ciclo
- Confirme configurações

### 4. Acompanhar Envio
- Receba notificações em tempo real
- Use botões para pausar/retomar
- Aguarde relatório final

## 📁 Estrutura do Projeto

```
botgerenciador/
├── main.py              # Arquivo principal
├── handlers.py          # Handlers do bot
├── utils.py             # Funções auxiliares
├── translations.py      # Sistema multilíngue
├── config.py           # Configurações
├── requirements.txt    # Dependências
├── .env.example       # Exemplo de configuração
├── backup.json        # Backup automático (gerado)
├── reports/           # Relatórios (gerado)
└── bot.log           # Logs (gerado)
```

## 🔧 Configurações Avançadas

### Backup Automático
- Salvo automaticamente a cada ciclo
- Recuperação automática em caso de falha
- Arquivo: `backup.json`

### Logs
- Logs detalhados em `bot.log`
- Níveis: INFO, WARNING, ERROR
- Rotação automática

### Relatórios
- Salvos em `reports/`
- Formato: `relatorio_envio_{user_id}_{timestamp}.csv`
- Colunas: api_key, chat_id, mensagem, status_envio, data_hora_envio, erro

## 🌐 Idiomas Suportados

| Código | Idioma | Status |
|--------|--------|--------|
| pt-BR  | Português (Brasil) | ✅ Completo |
| en-US  | English (US) | ✅ Completo |
| zh-CN  | 中文 (简体) | ✅ Completo |

## 🚨 Tratamento de Erros

### Erros de Envio
- ✅ Log detalhado do erro
- ✅ Notificação ao usuário
- ✅ Skip automático para próxima mensagem
- ✅ Continuidade do processo

### Erros de Sistema
- ✅ Backup automático preserva progresso
- ✅ Recuperação automática ao reiniciar
- ✅ Logs para diagnóstico

## 📊 Exemplo de Planilha

| api_key | chat_id | mensagem |
|---------|---------|----------|
| 123456:ABCDEF | -1001234567 | Olá! Como você está? 😊 |
| 654321:ZYXWVU | -1007654321 | Novidades incríveis! 🚀 |

## 🔒 Segurança

- ✅ Senha obrigatória para acesso
- ✅ Validação de arquivos
- ✅ Sanitização de dados
- ✅ Logs de auditoria
- ✅ Timeout em requisições

## 🆘 Suporte

### Comandos Disponíveis
- `/start` - Iniciar bot
- `/help` - Ajuda
- `/menu` - Voltar ao menu

### Botões Interativos
- ⏸️ Pausar - Pausa envio atual
- 🔄 Retomar - Retoma envio pausado
- ⏪ Voltar - Volta ao menu anterior
- ❌ Cancelar - Cancela operação atual
- 🔄 Reiniciar - Reinicia processo

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Contato

Para suporte ou dúvidas, entre em contato através do GitHub Issues.

---

**Desenvolvido com ❤️ para automação eficiente de mensagens Telegram**