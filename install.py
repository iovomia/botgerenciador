#!/usr/bin/env python3
"""
Script de instalação e configuração do Bot Telegram
Automatiza a configuração inicial do sistema
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Exibe banner do sistema"""
    print("=" * 60)
    print("🤖 BOT TELEGRAM - SISTEMA DE ENVIO AUTOMATIZADO")
    print("=" * 60)
    print("📋 Instalação e Configuração Automática")
    print("=" * 60)

def check_python_version():
    """Verifica versão do Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário!")
        print(f"   Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def install_dependencies():
    """Instala dependências"""
    print("\n📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências!")
        return False

def create_env_file():
    """Cria arquivo .env com configurações"""
    print("\n⚙️ Configurando arquivo .env...")
    
    if os.path.exists('.env'):
        response = input("📄 Arquivo .env já existe. Sobrescrever? (s/N): ")
        if response.lower() != 's':
            print("⏭️ Mantendo configuração existente")
            return True
    
    print("\n🔧 Configuração do Bot:")
    bot_token = input("🔑 Token do Bot Telegram: ").strip()
    
    if not bot_token:
        print("❌ Token é obrigatório!")
        return False
    
    password = input("🔐 Senha do sistema (padrão: kangoo@#2019): ").strip()
    if not password:
        password = "kangoo@#2019"
    
    admin_id = input("👤 ID do administrador (opcional): ").strip()
    
    # Criar arquivo .env
    env_content = f"""# Bot Token do Telegram
BOT_TOKEN={bot_token}

# Senha de acesso ao sistema
SYSTEM_PASSWORD={password}

# ID do usuário administrador (opcional)
ADMIN_USER_ID={admin_id}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Arquivo .env criado com sucesso!")
    return True

def create_directories():
    """Cria diretórios necessários"""
    print("\n📁 Criando diretórios...")
    
    directories = ['reports', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Diretório '{directory}' criado")
    
    return True

def test_configuration():
    """Testa configuração básica"""
    print("\n🧪 Testando configuração...")
    
    try:
        # Testar imports
        from config import BOT_TOKEN
        from utils import BackupManager
        from translations import get_text
        
        if not BOT_TOKEN:
            print("❌ BOT_TOKEN não configurado!")
            return False
        
        print("✅ Configuração básica OK")
        print("✅ Imports funcionando")
        print("✅ Sistema pronto para uso!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False

def show_usage_instructions():
    """Mostra instruções de uso"""
    print("\n" + "=" * 60)
    print("🚀 INSTALAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print("\n📋 Como usar:")
    print("1. Execute: python main.py")
    print("2. Envie /start para o bot no Telegram")
    print("3. Digite a senha configurada")
    print("4. Envie sua planilha (.csv ou .xlsx)")
    print("5. Configure intervalo e quantidade por ciclo")
    print("6. Inicie o envio!")
    
    print("\n🔧 Comandos disponíveis:")
    print("• /start - Iniciar bot")
    print("• /language - Mudar idioma")
    print("• /help - Ajuda")
    print("• /menu - Voltar ao menu")
    
    print("\n📊 Formato da planilha:")
    print("Colunas obrigatórias: api_key, chat_id, mensagem")
    
    print("\n🌍 Idiomas suportados:")
    print("• Português (PT-BR)")
    print("• English (EN-US)")
    print("• 中文 (ZH-CN)")
    
    print("\n📁 Arquivos importantes:")
    print("• backup.json - Backup automático")
    print("• reports/ - Relatórios de envio")
    print("• bot.log - Logs do sistema")
    
    print("\n" + "=" * 60)

def main():
    """Função principal de instalação"""
    print_banner()
    
    # Verificar Python
    if not check_python_version():
        return False
    
    # Instalar dependências
    if not install_dependencies():
        return False
    
    # Criar arquivo .env
    if not create_env_file():
        return False
    
    # Criar diretórios
    if not create_directories():
        return False
    
    # Testar configuração
    if not test_configuration():
        return False
    
    # Mostrar instruções
    show_usage_instructions()
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        if success:
            print("\n🎉 Instalação concluída com sucesso!")
            print("Execute 'python main.py' para iniciar o bot")
        else:
            print("\n❌ Instalação falhou!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Instalação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)