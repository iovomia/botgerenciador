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
        
        # Sistema de Templates de Mensagem
        'template_menu': '📝 **Gerenciar Mensagens**\n\nEscolha uma opção:',
        'create_template': '➕ **Criar Nova Mensagem**\n\nVamos criar uma mensagem personalizada!',
        'edit_template': '✏️ **Editar Mensagem: {name}**\n\nEscolha o que deseja editar:',
        'template_text_prompt': '📝 **Editar Texto**\n\nEnvie o texto da mensagem:',
        'template_photo_prompt': '🖼️ **Adicionar Foto**\n\nEnvie a foto que deseja incluir na mensagem:',
        'template_button_prompt': '🔘 **Adicionar Botão**\n\nEnvie no formato:\n`Texto do Botão | https://link.com`',
        'template_name_prompt': '💾 **Salvar Mensagem**\n\nDigite um nome para esta mensagem:',
        'template_saved': '✅ Mensagem "{name}" salva com sucesso!',
        'template_deleted': '🗑️ Mensagem "{name}" removida com sucesso!',
        'template_preview': '👁️ **Visualização da Mensagem:**\n\n{preview}',
        'template_selected': '✅ Mensagem "{name}" selecionada para envio!',
        'no_templates': '📝 Nenhuma mensagem salva ainda.\n\nCrie sua primeira mensagem!',
        'template_selection_prompt': '📝 Escolha uma mensagem para usar no envio:',
        'no_template': '📄 Usar mensagens da planilha',
        'no_template_selected': '✅ Usando mensagens da planilha!',
        
        # Sistema de Loop Infinito
        'loop_menu': '🔄 **Loop Infinito**\n\nConfiguração de envio contínuo:',
        'loop_enabled': '✅ Loop infinito ativado!\n\nAs mensagens serão enviadas continuamente.',
        'loop_disabled': '⏹️ Loop infinito desativado.',
        'loop_interval_prompt': '⚙️ **Configurar Intervalo**\n\nDigite o intervalo em minutos entre cada reinício:',
        'loop_status': '📊 **Status do Loop:**\n\n🔄 Ativo: {status}\n⏱️ Intervalo: {interval} min\n📝 Mensagem: {template}',
        'loop_restart': '🔄 Reiniciando envio automático...',
        'loop_finished_restart': '✅ Fila finalizada! Reiniciando em {interval} minutos...',
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
        
        # Message Templates
        'template_menu': '📝 **Manage Messages**\n\nChoose an option:',
        'create_template': '➕ **Create New Message**\n\nLet\'s create a custom message!',
        'edit_template': '✏️ **Edit Message: {name}**\n\nChoose what to edit:',
        'template_text_prompt': '📝 **Edit Text**\n\nSend the message text:',
        'template_photo_prompt': '🖼️ **Add Photo**\n\nSend the photo to include in the message:',
        'template_button_prompt': '🔘 **Add Button**\n\nSend in format:\n`Button Text | https://link.com`',
        'template_name_prompt': '💾 **Save Message**\n\nEnter a name for this message:',
        'template_saved': '✅ Message "{name}" saved successfully!',
        'template_deleted': '🗑️ Message "{name}" removed successfully!',
        'template_preview': '👁️ **Message Preview:**\n\n{preview}',
        'template_selected': '✅ Message "{name}" selected for sending!',
        'no_templates': '📝 No saved messages yet.\n\nCreate your first message!',
        'template_selection_prompt': '📝 Choose a message to use for sending:',
        'no_template': '📄 Use spreadsheet messages',
        'no_template_selected': '✅ Using spreadsheet messages!',
        
        # Infinite Loop System
        'loop_menu': '🔄 **Infinite Loop**\n\nContinuous sending configuration:',
        'loop_enabled': '✅ Infinite loop activated!\n\nMessages will be sent continuously.',
        'loop_disabled': '⏹️ Infinite loop disabled.',
        'loop_interval_prompt': '⚙️ **Configure Interval**\n\nEnter interval in minutes between each restart:',
        'loop_status': '📊 **Loop Status:**\n\n🔄 Active: {status}\n⏱️ Interval: {interval} min\n📝 Message: {template}',
        'loop_restart': '🔄 Restarting automatic sending...',
        'loop_finished_restart': '✅ Queue finished! Restarting in {interval} minutes...',
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
        
        # 消息模板系统
        'template_menu': '📝 **管理消息**\n\n选择一个选项：',
        'create_template': '➕ **创建新消息**\n\n让我们创建一个自定义消息！',
        'edit_template': '✏️ **编辑消息：{name}**\n\n选择要编辑的内容：',
        'template_text_prompt': '📝 **编辑文本**\n\n发送消息文本：',
        'template_photo_prompt': '🖼️ **添加照片**\n\n发送要包含在消息中的照片：',
        'template_button_prompt': '🔘 **添加按钮**\n\n按格式发送：\n`按钮文本 | https://link.com`',
        'template_name_prompt': '💾 **保存消息**\n\n为此消息输入名称：',
        'template_saved': '✅ 消息"{name}"保存成功！',
        'template_deleted': '🗑️ 消息"{name}"删除成功！',
        'template_preview': '👁️ **消息预览：**\n\n{preview}',
        'template_selected': '✅ 消息"{name}"已选择发送！',
        'no_templates': '📝 还没有保存的消息。\n\n创建您的第一条消息！',
        'template_selection_prompt': '📝 选择要用于发送的消息：',
        'no_template': '📄 使用电子表格消息',
        'no_template_selected': '✅ 使用电子表格消息！',
        
        # 无限循环系统
        'loop_menu': '🔄 **无限循环**\n\n连续发送配置：',
        'loop_enabled': '✅ 无限循环已激活！\n\n消息将连续发送。',
        'loop_disabled': '⏹️ 无限循环已禁用。',
        'loop_interval_prompt': '⚙️ **配置间隔**\n\n输入每次重启之间的间隔（分钟）：',
        'loop_status': '📊 **循环状态：**\n\n🔄 活动：{status}\n⏱️ 间隔：{interval} 分钟\n📝 消息：{template}',
        'loop_restart': '🔄 重启自动发送...',
        'loop_finished_restart': '✅ 队列完成！{interval} 分钟后重启...',
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