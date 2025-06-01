#!/usr/bin/env python3
"""
Bot Telegram para Envio Automatizado de Mensagens
Sistema completo com autenticação, backup, relatórios e interface multilíngue

Funcionalidades:
- Autenticação por senha
- Upload de planilhas (CSV/XLSX)
- Configuração de intervalos e lotes
- Envio automatizado com notificações
- Sistema de backup e recuperação
- Tratamento de erros com skip automático
- Relatórios detalhados
- Interface multilíngue (PT-BR, EN-US, ZH-CN)
- Navegação fluida com botões interativos
"""

import logging
import asyncio
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    CallbackQueryHandler, filters
)

from config import BOT_TOKEN
from handlers import BotHandlers

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

def main():
    """Função principal do bot"""
    
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN não configurado! Verifique o arquivo .env")
        return
    
    # Criar aplicação
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Registrar handlers
    application.add_handler(CommandHandler("start", BotHandlers.start_command))
    application.add_handler(CommandHandler("help", BotHandlers.start_command))
    application.add_handler(CommandHandler("menu", BotHandlers.start_command))
    application.add_handler(CommandHandler("language", BotHandlers.language_command))
    
    # Handler para mensagens de texto
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        BotHandlers.handle_message
    ))
    
    # Handler para documentos (planilhas)
    application.add_handler(MessageHandler(
        filters.Document.ALL,
        BotHandlers.handle_document
    ))
    
    # Handler para botões inline
    application.add_handler(CallbackQueryHandler(BotHandlers.handle_callback_query))
    
    # Iniciar bot
    logger.info("🚀 Bot iniciado com sucesso!")
    logger.info("📋 Funcionalidades ativas:")
    logger.info("   ✅ Autenticação por senha")
    logger.info("   ✅ Upload de planilhas CSV/XLSX")
    logger.info("   ✅ Sistema de backup automático")
    logger.info("   ✅ Envio com notificações em tempo real")
    logger.info("   ✅ Tratamento de erros com skip")
    logger.info("   ✅ Interface multilíngue (PT/EN/ZH)")
    logger.info("   ✅ Relatórios detalhados")
    logger.info("   ✅ Navegação com botões interativos")
    
    # Executar bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot interrompido pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        raise