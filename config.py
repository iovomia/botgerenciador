import os
from dotenv import load_dotenv

load_dotenv()

# Configurações do bot
BOT_TOKEN = os.getenv('BOT_TOKEN')
SYSTEM_PASSWORD = os.getenv('SYSTEM_PASSWORD', 'kangoo@#2019')
ADMIN_USER_ID = os.getenv('ADMIN_USER_ID')

# Configurações de backup
BACKUP_FILE = 'backup.json'
REPORTS_DIR = 'reports'

# Configurações de envio
DEFAULT_INTERVAL = 5  # minutos
DEFAULT_BATCH_SIZE = 10  # mensagens por ciclo
MAX_LOGIN_ATTEMPTS = 5

# Idiomas suportados
SUPPORTED_LANGUAGES = {
    'pt': 'pt-BR',
    'en': 'en-US', 
    'zh': 'zh-CN'
}

# Criar diretórios necessários
os.makedirs(REPORTS_DIR, exist_ok=True)