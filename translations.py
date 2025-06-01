"""
Sistema de traduções multilíngue
Suporta: Português (pt-BR), Inglês (en-US), Chinês Simplificado (zh-CN)
"""

TRANSLATIONS = {
    'pt-BR': {
        # Login
        'login_prompt': '🔐 Por favor, insira a senha para acessar o sistema.',
        'login_incorrect': '❌ Senha incorreta! Tente novamente.',
        'login_blocked': '🚫 Muitas tentativas incorretas. Acesso bloqueado temporariamente.',
        'login_success': '✅ Login realizado com sucesso!',
        
        # Upload
        'upload_prompt': '📥 Por favor, envie a planilha (.csv ou .xlsx) para iniciar o envio de mensagens.',
        'upload_existing': '⚠️ Já existe uma planilha carregada.\nDeseja:',
        'upload_replace': '✅ Substituir pela nova',
        'upload_continue': '🔄 Continuar de onde parou',
        'upload_cancel': '❌ Cancelar',
        'upload_success': '✅ Planilha carregada com sucesso!',
        'upload_error': '❌ Erro ao processar planilha. Verifique o formato.',
        
        # Configuração
        'config_interval': '⏱️ Informe o intervalo de envio (em minutos):',
        'config_batch': '✉️ Quantas mensagens deseja enviar a cada ciclo?',
        'config_summary': '📄 Mensagens na fila: {count}\n⏱️ Intervalo: {interval} min\n✉️ Por ciclo: {batch}',
        'config_start': '▶️ Iniciar envio',
        'config_reconfigure': '⚙️ Reconfigurar',
        'config_cancel': '❌ Cancelar',
        
        # Envio
        'send_success': '✅ Mensagem enviada com sucesso para: {chat_id}',
        'send_error': '⚠️ Erro ao enviar para: {chat_id}. Pulando para o próximo.',
        'send_paused': '⏸️ Envio pausado.',
        'send_resumed': '▶️ Envio retomado.',
        'send_cancelled': '❌ Envio cancelado.',
        
        # Backup
        'backup_detected': '🚀 Sistema detectou envio anterior inacabado.\nDeseja:',
        'backup_resume': '🔄 Retomar de onde parou',
        'backup_cancel': '❌ Cancelar',
        
        # Finalização
        'completion_success': '✅ Todas as mensagens foram enviadas com sucesso! 🎯',
        'completion_report': '📥 Aqui está o relatório final.',
        'completion_new_sheet': '📢 Por favor, envie uma nova planilha para atualizar a fila de mensagens.',
        
        # Botões
        'btn_pause': '⏸️ Pausar',
        'btn_resume': '🔄 Retomar',
        'btn_back': '⏪ Voltar ao Menu',
        'btn_cancel': '❌ Cancelar',
        'btn_restart': '🔄 Reiniciar',
        'btn_new_sheet': '📥 Enviar nova planilha',
        
        # Erros
        'error_invalid_file': '❌ Arquivo inválido. Envie apenas .csv ou .xlsx',
        'error_invalid_format': '❌ Formato da planilha inválido. Colunas necessárias: api_key, chat_id, mensagem',
        'error_invalid_number': '❌ Por favor, insira um número válido.',
        'error_general': '❌ Ocorreu um erro inesperado. Tente novamente.',
        
        # Status
        'status_processing': '⏳ Processando...',
        'status_waiting': '⏳ Aguardando próximo ciclo...',
        'status_queue_empty': '📭 Fila vazia. Envie uma nova planilha.',
    },
    
    'en-US': {
        # Login
        'login_prompt': '🔐 Please enter the password to access the system.',
        'login_incorrect': '❌ Incorrect password! Try again.',
        'login_blocked': '🚫 Too many incorrect attempts. Access temporarily blocked.',
        'login_success': '✅ Login successful!',
        
        # Upload
        'upload_prompt': '📥 Please send the spreadsheet (.csv or .xlsx) to start sending messages.',
        'upload_existing': '⚠️ A spreadsheet is already loaded.\nDo you want to:',
        'upload_replace': '✅ Replace with new one',
        'upload_continue': '🔄 Continue from where stopped',
        'upload_cancel': '❌ Cancel',
        'upload_success': '✅ Spreadsheet loaded successfully!',
        'upload_error': '❌ Error processing spreadsheet. Check the format.',
        
        # Configuration
        'config_interval': '⏱️ Enter the sending interval (in minutes):',
        'config_batch': '✉️ How many messages do you want to send per cycle?',
        'config_summary': '📄 Messages in queue: {count}\n⏱️ Interval: {interval} min\n✉️ Per cycle: {batch}',
        'config_start': '▶️ Start sending',
        'config_reconfigure': '⚙️ Reconfigure',
        'config_cancel': '❌ Cancel',
        
        # Sending
        'send_success': '✅ Message sent successfully to: {chat_id}',
        'send_error': '⚠️ Error sending to: {chat_id}. Skipping to next.',
        'send_paused': '⏸️ Sending paused.',
        'send_resumed': '▶️ Sending resumed.',
        'send_cancelled': '❌ Sending cancelled.',
        
        # Backup
        'backup_detected': '🚀 System detected unfinished previous sending.\nDo you want to:',
        'backup_resume': '🔄 Resume from where stopped',
        'backup_cancel': '❌ Cancel',
        
        # Completion
        'completion_success': '✅ All messages sent successfully! 🎯',
        'completion_report': '📥 Here is the final report.',
        'completion_new_sheet': '📢 Please send a new spreadsheet to update the message queue.',
        
        # Buttons
        'btn_pause': '⏸️ Pause',
        'btn_resume': '🔄 Resume',
        'btn_back': '⏪ Back to Menu',
        'btn_cancel': '❌ Cancel',
        'btn_restart': '🔄 Restart',
        'btn_new_sheet': '📥 Send new spreadsheet',
        
        # Errors
        'error_invalid_file': '❌ Invalid file. Send only .csv or .xlsx',
        'error_invalid_format': '❌ Invalid spreadsheet format. Required columns: api_key, chat_id, mensagem',
        'error_invalid_number': '❌ Please enter a valid number.',
        'error_general': '❌ An unexpected error occurred. Try again.',
        
        # Status
        'status_processing': '⏳ Processing...',
        'status_waiting': '⏳ Waiting for next cycle...',
        'status_queue_empty': '📭 Queue empty. Send a new spreadsheet.',
    },
    
    'zh-CN': {
        # Login
        'login_prompt': '🔐 请输入密码以访问系统。',
        'login_incorrect': '❌ 密码错误！请重试。',
        'login_blocked': '🚫 错误尝试次数过多。访问暂时被阻止。',
        'login_success': '✅ 登录成功！',
        
        # Upload
        'upload_prompt': '📥 请发送电子表格（.csv 或 .xlsx）开始发送消息。',
        'upload_existing': '⚠️ 已加载电子表格。\n您想要：',
        'upload_replace': '✅ 替换为新的',
        'upload_continue': '🔄 从停止的地方继续',
        'upload_cancel': '❌ 取消',
        'upload_success': '✅ 电子表格加载成功！',
        'upload_error': '❌ 处理电子表格时出错。请检查格式。',
        
        # Configuration
        'config_interval': '⏱️ 输入发送间隔（分钟）：',
        'config_batch': '✉️ 每个周期要发送多少条消息？',
        'config_summary': '📄 队列中的消息：{count}\n⏱️ 间隔：{interval} 分钟\n✉️ 每周期：{batch}',
        'config_start': '▶️ 开始发送',
        'config_reconfigure': '⚙️ 重新配置',
        'config_cancel': '❌ 取消',
        
        # Sending
        'send_success': '✅ 消息成功发送至：{chat_id}',
        'send_error': '⚠️ 发送至 {chat_id} 时出错。跳到下一个。',
        'send_paused': '⏸️ 发送已暂停。',
        'send_resumed': '▶️ 发送已恢复。',
        'send_cancelled': '❌ 发送已取消。',
        
        # Backup
        'backup_detected': '🚀 系统检测到未完成的先前发送。\n您想要：',
        'backup_resume': '🔄 从停止的地方恢复',
        'backup_cancel': '❌ 取消',
        
        # Completion
        'completion_success': '✅ 所有消息发送成功！🎯',
        'completion_report': '📥 这是最终报告。',
        'completion_new_sheet': '📢 请发送新的电子表格以更新消息队列。',
        
        # Buttons
        'btn_pause': '⏸️ 暂停',
        'btn_resume': '🔄 恢复',
        'btn_back': '⏪ 返回菜单',
        'btn_cancel': '❌ 取消',
        'btn_restart': '🔄ᅟ重启',
        'btn_new_sheet': '📥 发送新电子表格',
        
        # Errors
        'error_invalid_file': '❌ 无效文件。仅发送 .csv 或 .xlsx',
        'error_invalid_format': '❌ 电子表格格式无效。必需列：api_key, chat_id, mensagem',
        'error_invalid_number': '❌ 请输入有效数字。',
        'error_general': '❌ 发生意外错误。请重试。',
        
        # Status
        'status_processing': '⏳ 处理中...',
        'status_waiting': '⏳ 等待下一个周期...',
        'status_queue_empty': '📭 队列为空。发送新的电子表格。',
    }
}

def get_text(key: str, lang: str = 'pt-BR', **kwargs) -> str:
    """
    Obtém texto traduzido para o idioma especificado
    """
    if lang not in TRANSLATIONS:
        lang = 'pt-BR'  # fallback para português
    
    text = TRANSLATIONS[lang].get(key, TRANSLATIONS['pt-BR'].get(key, key))
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    
    return text

def detect_language(user_language_code: str) -> str:
    """
    Detecta o idioma baseado no código do usuário do Telegram
    """
    if user_language_code:
        if user_language_code.startswith('pt'):
            return 'pt-BR'
        elif user_language_code.startswith('en'):
            return 'en-US'
        elif user_language_code.startswith('zh'):
            return 'zh-CN'
    
    return 'pt-BR'  # padrão português