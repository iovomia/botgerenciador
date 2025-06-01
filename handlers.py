import asyncio
import os
import logging
from datetime import datetime
from typing import Dict, Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import SYSTEM_PASSWORD, MAX_LOGIN_ATTEMPTS
from translations import get_text, detect_language
from utils import (
    BackupManager, SpreadsheetProcessor, MessageSender, 
    ReportGenerator, UserSession, validate_number
)

logger = logging.getLogger(__name__)

# Instância global para gerenciar sessões
user_sessions = UserSession()

class BotHandlers:
    """Handlers principais do bot"""
    
    @staticmethod
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para comando /start"""
        user_id = str(update.effective_user.id)
        user_lang = detect_language(update.effective_user.language_code)
        
        session = user_sessions.get_session(user_id)
        user_sessions.update_session(user_id, {'language': user_lang})
        
        # Verificar se há backup
        backup_data = BackupManager.load_backup()
        if backup_data and backup_data.get('user_id') == user_id:
            await BotHandlers._show_backup_recovery(update, context, user_lang)
        else:
            await BotHandlers._show_login(update, context, user_lang)
    
    @staticmethod
    async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para comando /language"""
        user_id = str(update.effective_user.id)
        
        keyboard = [
            [InlineKeyboardButton("🇧🇷 Português", callback_data='lang_pt-BR')],
            [InlineKeyboardButton("🇺🇸 English", callback_data='lang_en-US')],
            [InlineKeyboardButton("🇨🇳 中文", callback_data='lang_zh-CN')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🌍 Escolha seu idioma / Choose your language / 选择语言:",
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def _show_login(update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
        """Mostra tela de login"""
        text = get_text('login_prompt', lang)
        await update.message.reply_text(text)
        
        user_id = str(update.effective_user.id)
        user_sessions.update_session(user_id, {'state': 'awaiting_password'})
    
    @staticmethod
    async def _show_backup_recovery(update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
        """Mostra opções de recuperação de backup"""
        text = get_text('backup_detected', lang)
        
        keyboard = [
            [InlineKeyboardButton(get_text('backup_resume', lang), callback_data='backup_resume')],
            [InlineKeyboardButton(get_text('backup_cancel', lang), callback_data='backup_cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup)
        
        user_id = str(update.effective_user.id)
        user_sessions.update_session(user_id, {'state': 'backup_recovery'})
    
    @staticmethod
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler principal para mensagens de texto"""
        user_id = str(update.effective_user.id)
        session = user_sessions.get_session(user_id)
        lang = session.get('language', 'pt-BR')
        state = session.get('state', 'login')
        
        if state == 'awaiting_password':
            await BotHandlers._handle_password(update, context, session, lang)
        elif state == 'awaiting_interval':
            await BotHandlers._handle_interval(update, context, session, lang)
        elif state == 'awaiting_batch_size':
            await BotHandlers._handle_batch_size(update, context, session, lang)
        else:
            # Estado não reconhecido, voltar ao início
            await BotHandlers._show_login(update, context, lang)
    
    @staticmethod
    async def _handle_password(update: Update, context: ContextTypes.DEFAULT_TYPE, session: Dict, lang: str):
        """Processa tentativa de login"""
        user_id = str(update.effective_user.id)
        password = update.message.text.strip()
        
        if password == SYSTEM_PASSWORD:
            user_sessions.update_session(user_id, {
                'authenticated': True,
                'state': 'authenticated',
                'login_attempts': 0
            })
            
            text = get_text('login_success', lang)
            await update.message.reply_text(text)
            
            # Mostrar upload de planilha
            await BotHandlers._show_upload_prompt(update, context, lang)
        else:
            attempts = session.get('login_attempts', 0) + 1
            user_sessions.update_session(user_id, {'login_attempts': attempts})
            
            if attempts >= MAX_LOGIN_ATTEMPTS:
                text = get_text('login_blocked', lang)
                await update.message.reply_text(text)
                user_sessions.clear_session(user_id)
            else:
                text = get_text('login_incorrect', lang)
                await update.message.reply_text(text)
    
    @staticmethod
    async def _show_upload_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
        """Mostra prompt para upload de planilha"""
        user_id = str(update.effective_user.id)
        session = user_sessions.get_session(user_id)
        
        # Verificar se já há mensagens na fila
        if session.get('messages_queue'):
            text = get_text('upload_existing', lang)
            keyboard = [
                [InlineKeyboardButton(get_text('upload_replace', lang), callback_data='upload_replace')],
                [InlineKeyboardButton(get_text('upload_continue', lang), callback_data='upload_continue')],
                [InlineKeyboardButton(get_text('upload_cancel', lang), callback_data='upload_cancel')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(text, reply_markup=reply_markup)
        else:
            text = get_text('upload_prompt', lang)
            await update.message.reply_text(text)
            user_sessions.update_session(user_id, {'state': 'awaiting_file'})
    
    @staticmethod
    async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para documentos (planilhas)"""
        user_id = str(update.effective_user.id)
        session = user_sessions.get_session(user_id)
        lang = session.get('language', 'pt-BR')
        
        if not session.get('authenticated'):
            await BotHandlers._show_login(update, context, lang)
            return
        
        document = update.message.document
        if not document.file_name.endswith(('.csv', '.xlsx', '.xls')):
            text = get_text('error_invalid_file', lang)
            await update.message.reply_text(text)
            return
        
        try:
            # Download do arquivo
            file = await context.bot.get_file(document.file_id)
            file_path = f"temp_{user_id}_{document.file_name}"
            await file.download_to_drive(file_path)
            
            # Processar planilha
            messages = SpreadsheetProcessor.process_file(file_path)
            
            # Remover arquivo temporário
            os.remove(file_path)
            
            if messages:
                user_sessions.update_session(user_id, {
                    'messages_queue': messages,
                    'state': 'file_uploaded'
                })
                
                text = get_text('upload_success', lang)
                await update.message.reply_text(text)
                
                # Mostrar configuração
                await BotHandlers._show_config_interval(update, context, lang)
            else:
                text = get_text('error_invalid_format', lang)
                await update.message.reply_text(text)
                
        except Exception as e:
            logger.error(f"Erro ao processar arquivo: {e}")
            text = get_text('upload_error', lang)
            await update.message.reply_text(text)
    
    @staticmethod
    async def _show_config_interval(update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
        """Mostra configuração de intervalo"""
        text = get_text('config_interval', lang)
        await update.message.reply_text(text)
        
        user_id = str(update.effective_user.id)
        user_sessions.update_session(user_id, {'state': 'awaiting_interval'})
    
    @staticmethod
    async def _handle_interval(update: Update, context: ContextTypes.DEFAULT_TYPE, session: Dict, lang: str):
        """Processa configuração de intervalo"""
        user_id = str(update.effective_user.id)
        interval = validate_number(update.message.text, min_val=1, max_val=1440)  # máximo 24h
        
        if interval:
            user_sessions.update_session(user_id, {
                'current_config': {'interval': interval}
            })
            
            text = get_text('config_batch', lang)
            await update.message.reply_text(text)
            user_sessions.update_session(user_id, {'state': 'awaiting_batch_size'})
        else:
            text = get_text('error_invalid_number', lang)
            await update.message.reply_text(text)
    
    @staticmethod
    async def _handle_batch_size(update: Update, context: ContextTypes.DEFAULT_TYPE, session: Dict, lang: str):
        """Processa configuração de tamanho do lote"""
        user_id = str(update.effective_user.id)
        batch_size = validate_number(update.message.text, min_val=1, max_val=100)
        
        if batch_size:
            config = session.get('current_config', {})
            config['batch_size'] = batch_size
            user_sessions.update_session(user_id, {'current_config': config})
            
            await BotHandlers._show_config_summary(update, context, lang)
        else:
            text = get_text('error_invalid_number', lang)
            await update.message.reply_text(text)
    
    @staticmethod
    async def _show_config_summary(update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
        """Mostra resumo da configuração"""
        user_id = str(update.effective_user.id)
        session = user_sessions.get_session(user_id)
        
        config = session.get('current_config', {})
        messages_count = len(session.get('messages_queue', []))
        
        text = get_text('config_summary', lang, 
                       count=messages_count,
                       interval=config.get('interval', 0),
                       batch=config.get('batch_size', 0))
        
        keyboard = [
            [InlineKeyboardButton(get_text('config_start', lang), callback_data='start_sending')],
            [InlineKeyboardButton(get_text('config_reconfigure', lang), callback_data='reconfigure')],
            [InlineKeyboardButton(get_text('config_cancel', lang), callback_data='cancel_config')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup)
        user_sessions.update_session(user_id, {'state': 'config_summary'})
    
    @staticmethod
    async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para botões inline"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(query.from_user.id)
        session = user_sessions.get_session(user_id)
        lang = session.get('language', 'pt-BR')
        
        data = query.data
        
        if data == 'backup_resume':
            await BotHandlers._resume_from_backup(query, context, lang)
        elif data == 'backup_cancel':
            BackupManager.clear_backup()
            await BotHandlers._show_login(query, context, lang)
        elif data == 'upload_replace':
            await BotHandlers._show_upload_prompt(query, context, lang)
        elif data == 'upload_continue':
            await BotHandlers._show_config_interval(query, context, lang)
        elif data == 'upload_cancel':
            await BotHandlers._show_upload_prompt(query, context, lang)
        elif data == 'start_sending':
            await BotHandlers._start_sending_process(query, context, lang)
        elif data == 'reconfigure':
            await BotHandlers._show_config_interval(query, context, lang)
        elif data == 'cancel_config':
            await BotHandlers._show_upload_prompt(query, context, lang)
        elif data == 'pause_sending':
            await BotHandlers._pause_sending(query, context, lang)
        elif data == 'resume_sending':
            await BotHandlers._resume_sending(query, context, lang)
        elif data == 'cancel_sending':
            await BotHandlers._cancel_sending(query, context, lang)
        elif data == 'back_to_menu':
            await BotHandlers._show_upload_prompt(query, context, lang)
        elif data.startswith('lang_'):
            # Mudança de idioma
            new_lang = data.replace('lang_', '')
            user_sessions.update_session(user_id, {'language': new_lang})
            
            text = get_text('login_success', new_lang)
            await query.edit_message_text(text)
            
            # Voltar ao estado atual
            if session.get('authenticated'):
                await BotHandlers._show_upload_prompt(query, context, new_lang)
            else:
                await BotHandlers._show_login(query, context, new_lang)
    
    @staticmethod
    async def _resume_from_backup(query, context: ContextTypes.DEFAULT_TYPE, lang: str):
        """Resume envio a partir do backup"""
        backup_data = BackupManager.load_backup()
        if backup_data:
            user_id = str(query.from_user.id)
            user_sessions.update_session(user_id, {
                'authenticated': True,
                'messages_queue': backup_data.get('messages_queue', []),
                'current_config': backup_data.get('current_config', {}),
                'state': 'sending'
            })
            
            text = get_text('send_resumed', lang)
            await query.edit_message_text(text)
            
            await BotHandlers._start_sending_process(query, context, lang)
    
    @staticmethod
    async def _start_sending_process(query, context: ContextTypes.DEFAULT_TYPE, lang: str):
        """Inicia processo de envio"""
        user_id = str(query.from_user.id)
        session = user_sessions.get_session(user_id)
        
        user_sessions.update_session(user_id, {
            'sending_active': True,
            'sending_paused': False,
            'state': 'sending'
        })
        
        # Salvar backup inicial
        backup_data = {
            'user_id': user_id,
            'messages_queue': session.get('messages_queue', []),
            'current_config': session.get('current_config', {}),
            'timestamp': datetime.now().isoformat()
        }
        BackupManager.save_backup(backup_data)
        
        # Iniciar envio em background
        asyncio.create_task(BotHandlers._sending_loop(context, user_id, lang))
        
        # Mostrar controles de envio
        await BotHandlers._show_sending_controls(query, context, lang)
    
    @staticmethod
    async def _show_sending_controls(query, context: ContextTypes.DEFAULT_TYPE, lang: str):
        """Mostra controles durante o envio"""
        keyboard = [
            [InlineKeyboardButton(get_text('btn_pause', lang), callback_data='pause_sending')],
            [InlineKeyboardButton(get_text('btn_back', lang), callback_data='back_to_menu')],
            [InlineKeyboardButton(get_text('btn_cancel', lang), callback_data='cancel_sending')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = get_text('status_processing', lang)
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    @staticmethod
    async def _sending_loop(context: ContextTypes.DEFAULT_TYPE, user_id: str, lang: str):
        """Loop principal de envio de mensagens"""
        session = user_sessions.get_session(user_id)
        processed_messages = []  # Lista para armazenar mensagens processadas
        
        while session.get('sending_active') and session.get('messages_queue'):
            if session.get('sending_paused'):
                await asyncio.sleep(5)  # Verificar a cada 5 segundos se foi retomado
                continue
            
            config = session.get('current_config', {})
            interval = config.get('interval', 5) * 60  # converter para segundos
            batch_size = config.get('batch_size', 10)
            
            # Enviar lote de mensagens
            messages_sent = 0
            messages_queue = session.get('messages_queue', [])
            
            for i in range(min(batch_size, len(messages_queue))):
                if not session.get('sending_active') or session.get('sending_paused'):
                    break
                
                message_data = messages_queue.pop(0)
                
                # Enviar mensagem
                result = MessageSender.send_message(
                    message_data['api_key'],
                    message_data['chat_id'],
                    message_data['mensagem']
                )
                
                # Atualizar status
                if result['success']:
                    message_data['status_envio'] = '✅ Enviado'
                    message_data['data_hora_envio'] = result['timestamp']
                    
                    # Notificar usuário
                    text = get_text('send_success', lang, chat_id=message_data['chat_id'])
                    try:
                        await context.bot.send_message(user_id, text)
                    except:
                        pass  # Ignorar erros de notificação
                else:
                    message_data['status_envio'] = f"❌ Erro: {result['error']}"
                    message_data['erro'] = result['error']
                    
                    # Notificar erro
                    text = get_text('send_error', lang, chat_id=message_data['chat_id'])
                    try:
                        await context.bot.send_message(user_id, text)
                    except:
                        pass
                
                # Adicionar à lista de processadas
                processed_messages.append(message_data)
                messages_sent += 1
                
                # Atualizar sessão
                user_sessions.update_session(user_id, {'messages_queue': messages_queue})
                
                # Salvar backup com mensagens processadas
                backup_data = {
                    'user_id': user_id,
                    'messages_queue': messages_queue,
                    'processed_messages': processed_messages,
                    'current_config': config,
                    'timestamp': datetime.now().isoformat()
                }
                BackupManager.save_backup(backup_data)
            
            # Verificar se ainda há mensagens
            if not messages_queue:
                await BotHandlers._finish_sending(context, user_id, lang)
                break
            
            # Aguardar intervalo
            if session.get('sending_active') and not session.get('sending_paused'):
                text = get_text('status_waiting', lang)
                try:
                    await context.bot.send_message(user_id, text)
                except:
                    pass
                
                await asyncio.sleep(interval)
    
    @staticmethod
    async def _finish_sending(context: ContextTypes.DEFAULT_TYPE, user_id: str, lang: str):
        """Finaliza processo de envio"""
        session = user_sessions.get_session(user_id)
        
        # Obter todas as mensagens processadas (incluindo as que deram erro)
        backup_data = BackupManager.load_backup()
        all_messages = []
        
        if backup_data and 'processed_messages' in backup_data:
            all_messages = backup_data['processed_messages']
        
        # Gerar relatório
        report_path = ReportGenerator.generate_report(all_messages, user_id)
        
        # Notificar conclusão
        text = get_text('completion_success', lang)
        await context.bot.send_message(user_id, text)
        
        # Enviar relatório
        if report_path and os.path.exists(report_path):
            text = get_text('completion_report', lang)
            await context.bot.send_document(
                user_id, 
                document=open(report_path, 'rb'),
                caption=text
            )
        
        # Solicitar nova planilha
        text = get_text('completion_new_sheet', lang)
        keyboard = [[InlineKeyboardButton(get_text('btn_new_sheet', lang), callback_data='upload_replace')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(user_id, text, reply_markup=reply_markup)
        
        # Limpar estado
        user_sessions.update_session(user_id, {
            'sending_active': False,
            'sending_paused': False,
            'messages_queue': [],
            'state': 'completed'
        })
        
        # Limpar backup
        BackupManager.clear_backup()
    
    @staticmethod
    async def _pause_sending(query, context: ContextTypes.DEFAULT_TYPE, lang: str):
        """Pausa o envio"""
        user_id = str(query.from_user.id)
        user_sessions.update_session(user_id, {'sending_paused': True})
        
        text = get_text('send_paused', lang)
        keyboard = [
            [InlineKeyboardButton(get_text('btn_resume', lang), callback_data='resume_sending')],
            [InlineKeyboardButton(get_text('btn_cancel', lang), callback_data='cancel_sending')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    @staticmethod
    async def _resume_sending(query, context: ContextTypes.DEFAULT_TYPE, lang: str):
        """Retoma o envio"""
        user_id = str(query.from_user.id)
        user_sessions.update_session(user_id, {'sending_paused': False})
        
        text = get_text('send_resumed', lang)
        await query.edit_message_text(text)
        
        # Mostrar controles novamente
        await BotHandlers._show_sending_controls(query, context, lang)
    
    @staticmethod
    async def _cancel_sending(query, context: ContextTypes.DEFAULT_TYPE, lang: str):
        """Cancela o envio"""
        user_id = str(query.from_user.id)
        user_sessions.update_session(user_id, {
            'sending_active': False,
            'sending_paused': False,
            'state': 'cancelled'
        })
        
        text = get_text('send_cancelled', lang)
        await query.edit_message_text(text)
        
        # Voltar ao menu
        await BotHandlers._show_upload_prompt(query, context, lang)