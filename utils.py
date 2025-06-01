import json
import pandas as pd
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import requests
from config import BACKUP_FILE, REPORTS_DIR
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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
    
    @staticmethod
    def send_template_message(api_key: str, chat_id: str, template: Dict[str, Any]) -> Dict[str, Any]:
        """
        Envia mensagem usando template (com foto, texto e botões)
        """
        try:
            # Se há foto, usar sendPhoto
            if template.get('photo'):
                url = f"https://api.telegram.org/bot{api_key}/sendPhoto"
                
                payload = {
                    'chat_id': chat_id,
                    'photo': template['photo'],
                    'caption': template.get('text', ''),
                    'parse_mode': 'HTML'
                }
                
                # Adicionar botões se existirem
                if template.get('buttons'):
                    keyboard = []
                    for button in template['buttons']:
                        keyboard.append([{
                            'text': button['text'],
                            'url': button['url']
                        }])
                    
                    payload['reply_markup'] = {
                        'inline_keyboard': keyboard
                    }
                
                response = requests.post(url, json=payload, timeout=30)
            
            else:
                # Apenas texto e botões
                url = f"https://api.telegram.org/bot{api_key}/sendMessage"
                
                payload = {
                    'chat_id': chat_id,
                    'text': template.get('text', 'Mensagem sem texto'),
                    'parse_mode': 'HTML'
                }
                
                # Adicionar botões se existirem
                if template.get('buttons'):
                    keyboard = []
                    for button in template['buttons']:
                        keyboard.append([{
                            'text': button['text'],
                            'url': button['url']
                        }])
                    
                    payload['reply_markup'] = {
                        'inline_keyboard': keyboard
                    }
                
                response = requests.post(url, json=payload, timeout=30)
            
            # Processar resposta
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


class MessageTemplate:
    """Classe para gerenciar templates de mensagens"""
    
    TEMPLATES_FILE = 'message_templates.json'
    
    @staticmethod
    def load_templates() -> Dict[str, Any]:
        """Carrega templates salvos"""
        try:
            if os.path.exists(MessageTemplate.TEMPLATES_FILE):
                with open(MessageTemplate.TEMPLATES_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Erro ao carregar templates: {e}")
            return {}
    
    @staticmethod
    def save_templates(templates: Dict[str, Any]) -> bool:
        """Salva templates"""
        try:
            with open(MessageTemplate.TEMPLATES_FILE, 'w', encoding='utf-8') as f:
                json.dump(templates, f, ensure_ascii=False, indent=2)
            logger.info("Templates salvos com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar templates: {e}")
            return False
    
    @staticmethod
    def create_template(name: str, template_data: Dict[str, Any]) -> bool:
        """Cria novo template"""
        templates = MessageTemplate.load_templates()
        templates[name] = {
            'text': template_data.get('text', ''),
            'photo': template_data.get('photo', ''),
            'buttons': template_data.get('buttons', []),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        return MessageTemplate.save_templates(templates)
    
    @staticmethod
    def update_template(name: str, template_data: Dict[str, Any]) -> bool:
        """Atualiza template existente"""
        templates = MessageTemplate.load_templates()
        if name in templates:
            templates[name].update({
                'text': template_data.get('text', templates[name].get('text', '')),
                'photo': template_data.get('photo', templates[name].get('photo', '')),
                'buttons': template_data.get('buttons', templates[name].get('buttons', [])),
                'updated_at': datetime.now().isoformat()
            })
            return MessageTemplate.save_templates(templates)
        return False
    
    @staticmethod
    def delete_template(name: str) -> bool:
        """Remove template"""
        templates = MessageTemplate.load_templates()
        if name in templates:
            del templates[name]
            return MessageTemplate.save_templates(templates)
        return False
    
    @staticmethod
    def get_template(name: str) -> Optional[Dict[str, Any]]:
        """Obtém template específico"""
        templates = MessageTemplate.load_templates()
        return templates.get(name)
    
    @staticmethod
    def list_templates() -> List[str]:
        """Lista nomes dos templates"""
        templates = MessageTemplate.load_templates()
        return list(templates.keys())


class MessageBuilder:
    """Classe para construir mensagens interativamente"""
    
    @staticmethod
    def create_template_keyboard() -> InlineKeyboardMarkup:
        """Cria teclado para seleção de templates"""
        templates = MessageTemplate.list_templates()
        keyboard = []
        
        # Templates existentes
        for template in templates:
            keyboard.append([
                InlineKeyboardButton(f"📝 {template}", callback_data=f"select_template_{template}"),
                InlineKeyboardButton("✏️", callback_data=f"edit_template_{template}"),
                InlineKeyboardButton("🗑️", callback_data=f"delete_template_{template}")
            ])
        
        # Opções principais
        keyboard.extend([
            [InlineKeyboardButton("➕ Criar Nova Mensagem", callback_data="create_new_template")],
            [InlineKeyboardButton("⏪ Voltar", callback_data="back_to_main")]
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_edit_keyboard(template_name: str = None) -> InlineKeyboardMarkup:
        """Cria teclado para edição de mensagem"""
        prefix = f"edit_{template_name}_" if template_name else "new_"
        
        keyboard = [
            [InlineKeyboardButton("📝 Editar Texto", callback_data=f"{prefix}text")],
            [InlineKeyboardButton("🖼️ Adicionar Foto", callback_data=f"{prefix}photo")],
            [InlineKeyboardButton("🔘 Adicionar Botões", callback_data=f"{prefix}buttons")],
            [
                InlineKeyboardButton("👁️ Visualizar", callback_data=f"{prefix}preview"),
                InlineKeyboardButton("💾 Salvar", callback_data=f"{prefix}save")
            ],
            [InlineKeyboardButton("⏪ Voltar", callback_data="back_to_templates")]
        ]
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_button_edit_keyboard(template_name: str = None) -> InlineKeyboardMarkup:
        """Cria teclado para edição de botões"""
        prefix = f"edit_{template_name}_" if template_name else "new_"
        
        keyboard = [
            [InlineKeyboardButton("➕ Adicionar Botão", callback_data=f"{prefix}add_button")],
            [InlineKeyboardButton("📋 Ver Botões", callback_data=f"{prefix}list_buttons")],
            [InlineKeyboardButton("🗑️ Limpar Botões", callback_data=f"{prefix}clear_buttons")],
            [InlineKeyboardButton("⏪ Voltar", callback_data=f"{prefix}back")]
        ]
        
        return InlineKeyboardMarkup(keyboard)


class LoopManager:
    """Classe para gerenciar envios em loop infinito"""
    
    LOOP_CONFIG_FILE = 'loop_config.json'
    
    @staticmethod
    def save_loop_config(user_id: str, config: Dict[str, Any]) -> bool:
        """Salva configuração de loop"""
        try:
            loop_configs = LoopManager.load_all_configs()
            loop_configs[user_id] = {
                'enabled': config.get('enabled', False),
                'interval_minutes': config.get('interval_minutes', 60),
                'messages_per_cycle': config.get('messages_per_cycle', 10),
                'template_name': config.get('template_name', ''),
                'restart_when_finished': config.get('restart_when_finished', True),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            with open(LoopManager.LOOP_CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(loop_configs, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Configuração de loop salva para usuário {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar configuração de loop: {e}")
            return False
    
    @staticmethod
    def load_loop_config(user_id: str) -> Optional[Dict[str, Any]]:
        """Carrega configuração de loop do usuário"""
        try:
            configs = LoopManager.load_all_configs()
            return configs.get(user_id)
        except Exception as e:
            logger.error(f"Erro ao carregar configuração de loop: {e}")
            return None
    
    @staticmethod
    def load_all_configs() -> Dict[str, Any]:
        """Carrega todas as configurações de loop"""
        try:
            if os.path.exists(LoopManager.LOOP_CONFIG_FILE):
                with open(LoopManager.LOOP_CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Erro ao carregar configurações de loop: {e}")
            return {}
    
    @staticmethod
    def is_loop_enabled(user_id: str) -> bool:
        """Verifica se loop está habilitado para usuário"""
        config = LoopManager.load_loop_config(user_id)
        return config.get('enabled', False) if config else False
    
    @staticmethod
    def disable_loop(user_id: str) -> bool:
        """Desabilita loop para usuário"""
        config = LoopManager.load_loop_config(user_id) or {}
        config['enabled'] = False
        config['updated_at'] = datetime.now().isoformat()
        return LoopManager.save_loop_config(user_id, config)
    
    @staticmethod
    def create_loop_keyboard() -> InlineKeyboardMarkup:
        """Cria teclado para configuração de loop"""
        keyboard = [
            [InlineKeyboardButton("🔄 Ativar Loop Infinito", callback_data="enable_loop")],
            [InlineKeyboardButton("⏹️ Desativar Loop", callback_data="disable_loop")],
            [InlineKeyboardButton("⚙️ Configurar Intervalo", callback_data="config_loop_interval")],
            [InlineKeyboardButton("📊 Status do Loop", callback_data="loop_status")],
            [InlineKeyboardButton("⏪ Voltar", callback_data="back_to_main")]
        ]
        
        return InlineKeyboardMarkup(keyboard)