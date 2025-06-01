# 📖 Manual Completo do Bot Telegram

## 🎯 Visão Geral

Este bot permite enviar mensagens automaticamente para grupos/canais do Telegram usando uma planilha com dados organizados. O sistema oferece controle total sobre o processo de envio, backup automático e relatórios detalhados.

## 🚀 Instalação Rápida

### 1. Preparação
```bash
git clone https://github.com/iovomia/botgerenciador.git
cd botgerenciador
python install.py
```

### 2. Configuração
- Insira o token do seu bot Telegram
- Defina a senha de acesso (padrão: `kangoo@#2019`)
- Configure ID do administrador (opcional)

### 3. Teste
```bash
python test_system.py
```

### 4. Execução
```bash
python main.py
```

## 📋 Fluxo de Uso Detalhado

### 🔐 1. Autenticação

**Primeiro acesso:**
1. Envie `/start` para o bot
2. Digite a senha: `kangoo@#2019` (ou a configurada)
3. Aguarde confirmação de login

**Recursos de segurança:**
- ✅ Máximo 5 tentativas de login
- ✅ Bloqueio temporário após erros
- ✅ Sessão persistente durante uso

### 📊 2. Upload da Planilha

**Formatos aceitos:**
- ✅ CSV (.csv)
- ✅ Excel (.xlsx, .xls)

**Estrutura obrigatória:**
| Coluna | Descrição | Exemplo |
|--------|-----------|---------|
| `api_key` | Token do bot que enviará | `123456:ABCDEF123456789` |
| `chat_id` | ID do grupo/canal | `-1001234567890` |
| `mensagem` | Texto a ser enviado | `Olá! Como você está? 😊` |

**Processo:**
1. Arraste e solte o arquivo no chat
2. Aguarde processamento automático
3. Confirme quantidade de mensagens detectadas

**Se já houver planilha carregada:**
- ✅ **Substituir**: Nova planilha substitui a anterior
- 🔄 **Continuar**: Retoma envio da planilha anterior
- ❌ **Cancelar**: Mantém planilha atual

### ⚙️ 3. Configuração de Envio

**Intervalo entre envios:**
- Mínimo: 1 minuto
- Máximo: 1440 minutos (24 horas)
- Recomendado: 5-10 minutos

**Mensagens por ciclo:**
- Mínimo: 1 mensagem
- Máximo: 100 mensagens
- Recomendado: 10-20 mensagens

**Exemplo de configuração:**
```
⏱️ Intervalo: 5 minutos
✉️ Por ciclo: 10 mensagens
📄 Total na fila: 150 mensagens
⏰ Tempo estimado: 75 minutos
```

### 🚀 4. Processo de Envio

**Início:**
1. Revise configurações no resumo
2. Clique em "▶️ Iniciar envio"
3. Acompanhe notificações em tempo real

**Durante o envio:**
- ✅ Notificação para cada mensagem enviada
- ⚠️ Alerta para mensagens com erro
- 📊 Progresso automático salvo

**Controles disponíveis:**
- ⏸️ **Pausar**: Para o envio temporariamente
- 🔄 **Retomar**: Continua envio pausado
- ⏪ **Voltar**: Retorna ao menu principal
- ❌ **Cancelar**: Interrompe definitivamente

### 💾 5. Sistema de Backup

**Backup automático:**
- ✅ Salvo a cada mensagem enviada
- ✅ Inclui posição atual na fila
- ✅ Preserva configurações
- ✅ Arquivo: `backup.json`

**Recuperação automática:**
- 🚀 Detecta envio interrompido
- 🔄 Oferece retomada automática
- ✅ Mantém histórico de envios

### 📈 6. Relatórios

**Relatório final:**
- 📊 Arquivo CSV detalhado
- ✅ Status de cada mensagem
- ⏰ Timestamp de envio
- ❌ Detalhes de erros

**Colunas do relatório:**
| Coluna | Descrição |
|--------|-----------|
| `api_key` | Token usado |
| `chat_id` | Destino da mensagem |
| `mensagem` | Conteúdo enviado |
| `status_envio` | ✅ Enviado ou ❌ Erro |
| `data_hora_envio` | Timestamp do envio |
| `erro` | Descrição do erro (se houver) |

## 🌍 Sistema Multilíngue

### Idiomas Suportados
- 🇧🇷 **Português (PT-BR)** - Padrão
- 🇺🇸 **English (EN-US)**
- 🇨🇳 **中文 (ZH-CN)**

### Mudança de Idioma
1. Comando: `/language`
2. Selecione idioma desejado
3. Interface atualizada automaticamente

### Detecção Automática
- ✅ Baseada no idioma do Telegram
- ✅ Fallback para português
- ✅ Persistente durante sessão

## 🔧 Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `/start` | Inicia o bot |
| `/help` | Mostra ajuda |
| `/menu` | Volta ao menu principal |
| `/language` | Muda idioma da interface |

## 🚨 Tratamento de Erros

### Erros de Envio
**Tipos comuns:**
- ❌ Token inválido
- ❌ Chat não encontrado
- ❌ Bot bloqueado no grupo
- ❌ Limite de rate exceeded

**Comportamento:**
- ✅ Log detalhado do erro
- ✅ Notificação ao usuário
- ✅ Skip automático para próxima
- ✅ Continuidade do processo

### Erros de Sistema
**Recuperação automática:**
- 💾 Backup preserva progresso
- 🔄 Retomada automática
- 📝 Logs para diagnóstico

## 📁 Estrutura de Arquivos

```
botgerenciador/
├── main.py              # Arquivo principal
├── handlers.py          # Lógica do bot
├── utils.py             # Funções auxiliares
├── translations.py      # Sistema multilíngue
├── config.py           # Configurações
├── install.py          # Script de instalação
├── test_system.py      # Testes do sistema
├── requirements.txt    # Dependências
├── .env               # Configurações (criado)
├── backup.json        # Backup automático (criado)
├── reports/           # Relatórios (criado)
├── bot.log           # Logs do sistema (criado)
└── example_spreadsheet.csv # Exemplo
```

## 🔒 Segurança e Boas Práticas

### Segurança
- ✅ Autenticação obrigatória
- ✅ Validação de arquivos
- ✅ Sanitização de dados
- ✅ Timeout em requisições
- ✅ Logs de auditoria

### Boas Práticas
- 📊 Teste com poucos dados primeiro
- ⏰ Use intervalos adequados (5+ min)
- 📝 Mantenha backup das planilhas
- 🔍 Monitore logs regularmente
- 📈 Analise relatórios de envio

### Limites Recomendados
- **Intervalo mínimo**: 5 minutos
- **Lote máximo**: 20 mensagens
- **Planilha máxima**: 1000 linhas por vez
- **Monitoramento**: Verificar a cada hora

## 🆘 Solução de Problemas

### Problemas Comuns

**Bot não responde:**
1. Verifique token no `.env`
2. Confirme que bot está ativo
3. Reinicie com `python main.py`

**Erro ao processar planilha:**
1. Verifique colunas obrigatórias
2. Confirme formato (CSV/XLSX)
3. Remova linhas vazias

**Mensagens não enviadas:**
1. Verifique API keys
2. Confirme IDs dos grupos
3. Teste bot manualmente nos grupos

**Backup corrompido:**
1. Delete `backup.json`
2. Reinicie processo
3. Reenvie planilha

### Logs e Diagnóstico

**Arquivo de log:** `bot.log`
```bash
tail -f bot.log  # Monitorar em tempo real
```

**Níveis de log:**
- `INFO`: Operações normais
- `WARNING`: Situações de atenção
- `ERROR`: Erros que precisam correção

## 📞 Suporte

### Recursos de Ajuda
- 📖 Este manual
- 🧪 Script de teste: `python test_system.py`
- 📝 Logs detalhados em `bot.log`
- 💬 Issues no GitHub

### Informações para Suporte
Ao reportar problemas, inclua:
1. Versão do Python
2. Sistema operacional
3. Conteúdo do arquivo `.env` (sem tokens)
4. Últimas linhas do `bot.log`
5. Descrição detalhada do problema

## 🔄 Atualizações

### Verificar Atualizações
```bash
git pull origin main
pip install -r requirements.txt
```

### Backup Antes de Atualizar
```bash
cp .env .env.backup
cp backup.json backup.json.backup
```

---

**📧 Desenvolvido com ❤️ para automação eficiente de mensagens Telegram**