#!/usr/bin/env python3
"""
Script de teste do sistema
Verifica se todos os componentes estão funcionando corretamente
"""

import os
import sys
import json
import tempfile
import pandas as pd
from datetime import datetime

def test_imports():
    """Testa imports dos módulos"""
    print("🧪 Testando imports...")
    
    try:
        import config
        import utils
        import translations
        import handlers
        print("✅ Todos os imports OK")
        return True
    except ImportError as e:
        print(f"❌ Erro no import: {e}")
        return False

def test_translations():
    """Testa sistema de traduções"""
    print("🌍 Testando traduções...")
    
    try:
        from translations import get_text, detect_language
        
        # Testar português
        text_pt = get_text('login_prompt', 'pt-BR')
        assert '🔐' in text_pt
        
        # Testar inglês
        text_en = get_text('login_prompt', 'en-US')
        assert 'password' in text_en.lower()
        
        # Testar chinês
        text_zh = get_text('login_prompt', 'zh-CN')
        assert '🔐' in text_zh
        
        # Testar detecção de idioma
        assert detect_language('pt-BR') == 'pt-BR'
        assert detect_language('en-US') == 'en-US'
        assert detect_language('zh-CN') == 'zh-CN'
        assert detect_language('fr') == 'pt-BR'  # fallback
        
        print("✅ Sistema de traduções OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro nas traduções: {e}")
        return False

def test_backup_system():
    """Testa sistema de backup"""
    print("💾 Testando sistema de backup...")
    
    try:
        from utils import BackupManager
        
        # Dados de teste
        test_data = {
            'user_id': 'test_user',
            'messages_queue': [
                {'api_key': 'test', 'chat_id': 'test', 'mensagem': 'test'}
            ],
            'timestamp': datetime.now().isoformat()
        }
        
        # Testar salvamento
        assert BackupManager.save_backup(test_data)
        
        # Testar carregamento
        loaded_data = BackupManager.load_backup()
        assert loaded_data is not None
        assert loaded_data['user_id'] == 'test_user'
        
        # Testar limpeza
        assert BackupManager.clear_backup()
        
        print("✅ Sistema de backup OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro no backup: {e}")
        return False

def test_spreadsheet_processor():
    """Testa processador de planilhas"""
    print("📊 Testando processador de planilhas...")
    
    try:
        from utils import SpreadsheetProcessor
        
        # Criar planilha de teste
        test_data = {
            'api_key': ['123:ABC', '456:DEF'],
            'chat_id': ['-1001', '-1002'],
            'mensagem': ['Teste 1', 'Teste 2']
        }
        
        df = pd.DataFrame(test_data)
        
        # Testar CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            csv_file = f.name
        
        messages = SpreadsheetProcessor.process_file(csv_file)
        assert messages is not None
        assert len(messages) == 2
        assert messages[0]['api_key'] == '123:ABC'
        
        os.unlink(csv_file)
        
        # Testar XLSX
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            df.to_excel(f.name, index=False)
            xlsx_file = f.name
        
        messages = SpreadsheetProcessor.process_file(xlsx_file)
        assert messages is not None
        assert len(messages) == 2
        
        os.unlink(xlsx_file)
        
        print("✅ Processador de planilhas OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro no processador: {e}")
        return False

def test_message_sender():
    """Testa simulação de envio de mensagens"""
    print("📤 Testando simulação de envio...")
    
    try:
        from utils import MessageSender
        
        # Testar com API key inválida (deve retornar erro)
        result = MessageSender.send_message(
            'invalid_key',
            'invalid_chat',
            'Mensagem de teste'
        )
        
        assert not result['success']
        assert 'error' in result
        
        print("✅ Simulação de envio OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro no envio: {e}")
        return False

def test_report_generator():
    """Testa gerador de relatórios"""
    print("📋 Testando gerador de relatórios...")
    
    try:
        from utils import ReportGenerator
        
        # Dados de teste
        test_messages = [
            {
                'api_key': '123:ABC',
                'chat_id': '-1001',
                'mensagem': 'Teste 1',
                'status_envio': '✅ Enviado',
                'data_hora_envio': datetime.now().isoformat(),
                'erro': None
            },
            {
                'api_key': '456:DEF',
                'chat_id': '-1002',
                'mensagem': 'Teste 2',
                'status_envio': '❌ Erro',
                'data_hora_envio': None,
                'erro': 'Teste de erro'
            }
        ]
        
        # Gerar relatório
        report_path = ReportGenerator.generate_report(test_messages, 'test_user')
        
        assert report_path is not None
        assert os.path.exists(report_path)
        
        # Verificar conteúdo
        df = pd.read_csv(report_path)
        assert len(df) == 2
        assert 'api_key' in df.columns
        
        # Limpar arquivo de teste
        os.unlink(report_path)
        
        print("✅ Gerador de relatórios OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro no gerador: {e}")
        return False

def test_user_session():
    """Testa sistema de sessões"""
    print("👤 Testando sistema de sessões...")
    
    try:
        from utils import UserSession
        
        session_manager = UserSession()
        
        # Testar criação de sessão
        session = session_manager.get_session('test_user')
        assert session is not None
        assert not session['authenticated']
        
        # Testar atualização
        session_manager.update_session('test_user', {'authenticated': True})
        updated_session = session_manager.get_session('test_user')
        assert updated_session['authenticated']
        
        # Testar limpeza
        session_manager.clear_session('test_user')
        assert 'test_user' not in session_manager.sessions
        
        print("✅ Sistema de sessões OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro nas sessões: {e}")
        return False

def test_utilities():
    """Testa funções utilitárias"""
    print("🔧 Testando utilitários...")
    
    try:
        from utils import validate_number, format_duration, sanitize_filename
        
        # Testar validação de números
        assert validate_number('5') == 5
        assert validate_number('0') is None
        assert validate_number('abc') is None
        assert validate_number('10', max_val=5) is None
        
        # Testar formatação de duração
        assert format_duration(30) == '30s'
        assert format_duration(120) == '2m'
        assert format_duration(3661) == '1h 1m'
        
        # Testar sanitização de nomes
        assert sanitize_filename('test<>file.txt') == 'test__file.txt'
        
        print("✅ Utilitários OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro nos utilitários: {e}")
        return False

def run_all_tests():
    """Executa todos os testes"""
    print("🧪 INICIANDO TESTES DO SISTEMA")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_translations,
        test_backup_system,
        test_spreadsheet_processor,
        test_message_sender,
        test_report_generator,
        test_user_session,
        test_utilities
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Erro inesperado em {test.__name__}: {e}")
            failed += 1
        print()
    
    print("=" * 50)
    print(f"📊 RESULTADOS: {passed} ✅ | {failed} ❌")
    
    if failed == 0:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema pronto para uso!")
        return True
    else:
        print("⚠️ Alguns testes falharam!")
        print("🔧 Verifique a configuração antes de usar")
        return False

if __name__ == '__main__':
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Testes cancelados pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)