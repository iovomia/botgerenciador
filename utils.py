import json
import pandas as pd
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import requests
from config import BACKUP_FILE, REPORTS_DIR

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BackupManager:
    """Gerencia backup e recuperação do estado do bot"""
    
    @staticmethod
    def save_backup(data: Dict[str, Any]) -> bool:
        """Salva backup do estado atual"""
        try:
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'data': data
            }
            with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)
            logger.info("Backup salvo com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar backup: {e}")
            return False
    
    @staticmethod
    def load_backup() -> Optional[Dict[str, Any]]:
        """Carrega backup se existir"""
        try:
            if os.path.exists(BACKUP_FILE):
                with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
                    backup_data = json.load(f)
                logger.info("Backup carregado com sucesso")
                return backup_data.get('data')
        except Exception as e:
            logger.error(f"Erro ao carregar backup: {e}")
        return None
    
    @staticmethod
    def clear_backup() -> bool:
        """Remove arquivo de backup"""
        try:
            if os.path.exists(BACKUP_FILE):
                os.remove(BACKUP_FILE)
                logger.info("Backup removido")
            return True
        except Exception as e:
            logger.error(f"Erro ao remover backup: {e}")
            return False

class SpreadsheetProcessor:
    """Processa planilhas CSV e XLSX"""
    
    @staticmethod
    def process_file(file_path: str) -> Optional[List[Dict[str, str]]]:
        """
        Processa arquivo de planilha e retorna lista de mensagens
        Formato esperado: api_key, chat_id, mensagem
        """
        try:
            # Detectar tipo de arquivo
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                logger.error("Formato de arquivo não suportado")
                return None
            
            # Verificar colunas obrigatórias
            required_columns = ['api_key', 'chat_id', 'mensagem']
            if not all(col in df.columns for col in required_columns):
                logger.error(f"Colunas obrigatórias não encontradas: {required_columns}")
                return None
            
            # Converter para lista de dicionários
            messages = []
            for _, row in df.iterrows():
                if pd.notna(row['api_key']) and pd.notna(row['chat_id']) and pd.notna(row['mensagem']):
                    messages.append({
                        'api_key': str(row['api_key']).strip(),
                        'chat_id': str(row['chat_id']).strip(),
                        'mensagem': str(row['mensagem']).strip(),
                        'status_envio': 'Pendente',
                        'data_hora_envio': None,
                        'erro': None
                    })
            
            logger.info(f"Processadas {len(messages)} mensagens da planilha")
            return messages
            
        except Exception as e:
            logger.error(f"Erro ao processar planilha: {e}")
            return None

class MessageSender:
    """Envia mensagens via API do Telegram"""
    
    @staticmethod
    def send_message(api_key: str, chat_id: str, message: str) -> Dict[str, Any]:
        """
        Envia mensagem via API do Telegram
        Retorna dict com status e informações do envio
        """
        try:
            url = f"https://api.telegram.org/bot{api_key}/sendMessage"
            
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    return {
                        'success': True,
                        'message_id': result.get('result', {}).get('message_id'),
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    return {
                        'success': False,
                        'error': result.get('description', 'Erro desconhecido'),
                        'error_code': result.get('error_code'),
                        'timestamp': datetime.now().isoformat()
                    }
            else:
                return {
                    'success': False,
                    'error': f'HTTP {response.status_code}: {response.text}',
                    'timestamp': datetime.now().isoformat()
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Timeout na requisição',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

class ReportGenerator:
    """Gera relatórios de envio"""
    
    @staticmethod
    def generate_report(messages: List[Dict[str, Any]], user_id: str) -> str:
        """
        Gera relatório CSV com resultados do envio
        Retorna caminho do arquivo gerado
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"relatorio_envio_{user_id}_{timestamp}.csv"
            filepath = os.path.join(REPORTS_DIR, filename)
            
            # Criar DataFrame
            df = pd.DataFrame(messages)
            
            # Adicionar estatísticas
            total = len(messages)
            enviados = len([m for m in messages if m.get('status_envio') == '✅ Enviado'])
            erros = total - enviados
            
            # Salvar CSV
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            logger.info(f"Relatório gerado: {filepath}")
            logger.info(f"Total: {total}, Enviados: {enviados}, Erros: {erros}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {e}")
            return None

class UserSession:
    """Gerencia sessões de usuário"""
    
    def __init__(self):
        self.sessions = {}
    
    def get_session(self, user_id: str) -> Dict[str, Any]:
        """Obtém sessão do usuário"""
        if user_id not in self.sessions:
            self.sessions[user_id] = {
                'authenticated': False,
                'language': 'pt-BR',
                'login_attempts': 0,
                'state': 'login',
                'messages_queue': [],
                'current_config': {},
                'sending_active': False,
                'sending_paused': False,
                'last_activity': datetime.now().isoformat()
            }
        return self.sessions[user_id]
    
    def update_session(self, user_id: str, updates: Dict[str, Any]):
        """Atualiza sessão do usuário"""
        session = self.get_session(user_id)
        session.update(updates)
        session['last_activity'] = datetime.now().isoformat()
    
    def clear_session(self, user_id: str):
        """Limpa sessão do usuário"""
        if user_id in self.sessions:
            del self.sessions[user_id]

def validate_number(text: str, min_val: int = 1, max_val: int = None) -> Optional[int]:
    """Valida se texto é um número válido dentro dos limites"""
    try:
        num = int(text)
        if num < min_val:
            return None
        if max_val and num > max_val:
            return None
        return num
    except ValueError:
        return None

def format_duration(seconds: int) -> str:
    """Formata duração em segundos para formato legível"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

def sanitize_filename(filename: str) -> str:
    """Remove caracteres inválidos do nome do arquivo"""
    import re
    return re.sub(r'[<>:"/\\|?*]', '_', filename)