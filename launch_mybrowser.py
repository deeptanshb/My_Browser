#!/usr/bin/env python3
"""
My Browser Launcher - Complete Edition
Features:
- AI Chatbot (Ollama integration)
- Microservices (Network Monitor, IP Masking, Social Tabs, Security Dashboard)
- CORS Proxy Management
- Comprehensive Logging
"""
import os

os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer"
os.environ["QT_OPENGL"] = "software"

import sys
import os
import logging
from datetime import datetime
import subprocess
import time
import atexit

# Change to script directory first
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Setup logging to file and terminal
log_dir = os.path.expanduser("~/.mybrowser/logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"browser_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Global variable for proxy process
proxy_process = None

def cleanup_proxy():
    """Clean up proxy process on exit"""
    global proxy_process
    if proxy_process:
        logger.info("🛑 Stopping CORS proxy...")
        try:
            proxy_process.terminate()
            proxy_process.wait(timeout=5)
            logger.info("✅ CORS proxy stopped")
        except:
            try:
                proxy_process.kill()
            except:
                pass

atexit.register(cleanup_proxy)

def check_ollama_running():
    """Check if Ollama is running"""
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data.get('models'):
                return True, data['models']
        return False, []
    except:
        return False, []

def start_cors_proxy():
    """Start the CORS proxy if Ollama is running"""
    global proxy_process
    
    proxy_file = os.path.join(script_dir, 'ollama_cors_proxy.py')
    if not os.path.exists(proxy_file):
        logger.warning("⚠️  ollama_cors_proxy.py not found - AI features may not work")
        return False
    
    try:
        proxy_log = os.path.join(log_dir, f"proxy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        with open(proxy_log, 'w') as log:
            proxy_process = subprocess.Popen(
                [sys.executable, proxy_file],
                stdout=log,
                stderr=subprocess.STDOUT,
                start_new_session=True
            )
        
        time.sleep(2)
        
        if proxy_process.poll() is None:
            try:
                import requests
                response = requests.get('http://localhost:8081/api/tags', timeout=2)
                if response.status_code == 200:
                    logger.info(f"✅ CORS proxy started (PID: {proxy_process.pid})")
                    logger.info(f"📝 Proxy log: {proxy_log}")
                    return True
            except:
                pass
        
        logger.warning("⚠️  CORS proxy failed to start")
        proxy_process = None
        return False
        
    except Exception as e:
        logger.warning(f"⚠️  Could not start CORS proxy: {e}")
        proxy_process = None
        return False

def check_microservices():
    """Check if microservices modules are available"""
    modules_dir = os.path.join(script_dir, 'modules')
    if not os.path.exists(modules_dir):
        return False, []
    
    required_modules = [
        '__init__.py',
        'network_interceptor.py',
        'ip_masking.py',
        'social_tabs.py',
        'security_monitor.py'
    ]
    
    found_modules = []
    missing_modules = []
    
    for module in required_modules:
        module_path = os.path.join(modules_dir, module)
        if os.path.exists(module_path):
            found_modules.append(module)
        else:
            missing_modules.append(module)
    
    return len(missing_modules) == 0, found_modules

def check_dependencies():
    """Check if required dependencies are installed"""
    missing = []
    
    # Check PyQt6
    try:
        from PyQt6.QtWidgets import QApplication
        logger.info("✅ PyQt6 found")
    except ImportError:
        missing.append("PyQt6")
    
    # Check Flask (for CORS proxy)
    try:
        import flask
        import flask_cors
        import requests
        logger.info("✅ Flask dependencies found")
    except ImportError:
        logger.warning("⚠️  Flask dependencies missing - AI features may not work")
        logger.info("   Install with: pip3 install flask flask-cors requests")
    
    return missing

# ============================================
# MAIN LAUNCHER
# ============================================

logger.info("=" * 70)
logger.info("🦕 MY BROWSER - COMPLETE EDITION")
logger.info("   AI Chatbot + Advanced Security Microservices")
logger.info("=" * 70)
logger.info(f"📂 Working directory: {os.getcwd()}")
logger.info(f"📝 Log file: {log_file}")
logger.info(f"🕐 Starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
logger.info("")

try:
    # Check dependencies
    logger.info("🔍 Checking dependencies...")
    missing_deps = check_dependencies()
    
    if missing_deps:
        logger.error(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        print("\n" + "=" * 70)
        print("ERROR: Missing dependencies!")
        print("=" * 70)
        for dep in missing_deps:
            if dep == "PyQt6":
                print("Install: sudo apt install python3-pyqt6 python3-pyqt6.qtwebengine")
        print("=" * 70)
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Check Microservices
    logger.info("")
    logger.info("🔧 Checking microservices modules...")
    microservices_ok, found_modules = check_microservices()
    
    if microservices_ok:
        logger.info(f"✅ All microservices modules found ({len(found_modules)} files)")
        logger.info("   📱 Social Media Quick Access")
        logger.info("   🎭 IP Masking Monitor")
        logger.info("   🌐 Network Request Interceptor")
        logger.info("   🛡️  Security Dashboard")
    else:
        logger.warning("⚠️  Microservices modules not found or incomplete")
        logger.info("   Browser will run with basic features only")
    
    # Check Ollama status
    logger.info("")
    logger.info("🔡 Checking Ollama status...")
    ollama_running, models = check_ollama_running()
    
    if ollama_running:
        logger.info(f"✅ Ollama is running with {len(models)} model(s)")
        for model in models[:3]:
            logger.info(f"   • {model.get('name', 'unknown')}")
        
        logger.info("")
        logger.info("🚀 Starting CORS proxy for AI features...")
        proxy_started = start_cors_proxy()
        
        if proxy_started:
            logger.info("✅ AI chatbot fully enabled")
        else:
            logger.warning("⚠️  CORS proxy failed - AI may have limited functionality")
    else:
        logger.warning("⚠️  Ollama not running")
        logger.info("   AI chatbot will be in fallback mode")
        logger.info("   To enable: run 'ollama serve' in another terminal")
    
    # Import and run browser
    logger.info("")
    logger.info("📦 Loading browser modules...")
    
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QFont
    logger.info("✅ PyQt6 loaded")
    
    logger.info(f"📥 Importing browser from custom.py...")

    # Apply proxy to Chromium before import
    try:
        import json as _json
        _sf = os.path.expanduser("~/.mybrowser/settings.json")
        with open(_sf) as _f:
            _s = _json.load(_f)
        if _s.get('proxy_enabled') and _s.get('proxy_host'):
            _ph = _s['proxy_host'].strip()
            _pp = str(_s.get('proxy_port', 9050))
            if _ph.startswith('socks5://'):
                _proxy_flag = f'--proxy-server={_ph}'
            elif _ph.startswith('http://'):
                _proxy_flag = f'--proxy-server={_ph}:{_pp}'
            else:
                _proxy_flag = f'--proxy-server=socks5://{_ph}:{_pp}'
            existing = os.environ.get('QTWEBENGINE_CHROMIUM_FLAGS', '')
            os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = existing + ' ' + _proxy_flag
            logger.info(f"🔒 Proxy applied to Chromium: {_proxy_flag}")
    except Exception as _e:
        logger.info(f"Proxy load skipped: {_e}")

    from custom import ModernBrowser
    
    logger.info("🎨 Initializing Qt Application...")
    app = QApplication(sys.argv)
    app.setApplicationName("My Browser - Complete Edition")
    app.setOrganizationName("MyBrowser")
    
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    app.setStyleSheet("* { color: black; } QComboBox { color: black; background: white; } QComboBox QAbstractItemView { color: black; background: white; } QMenu { color: black; background: white; } QMenu::item:selected { color: white; background: #6c63ff; } QTabBar::tab { color: black; } QLabel { color: black; }")
    app.setStyleSheet("QComboBox QAbstractItemView { background-color: white; color: black; } QComboBox { color: black; background-color: white; } QMenu { background-color: white; color: black; } QMenu::item:selected { background-color: #6c63ff; color: white; } QTabBar::tab { color: black; } QTabBar::tab:selected { color: black; }")
    app.setStyleSheet("QComboBox QAbstractItemView { background-color: white; color: black; selection-background-color: #6c63ff; selection-color: white; } QComboBox { color: black; background-color: white; } QMenu { background-color: white; color: black; } QMenu::item:selected { background-color: #6c63ff; color: white; }")
    
    logger.info("🪟 Creating browser window...")
    window = ModernBrowser()
    
    logger.info("✅ Browser successfully initialized!")
    logger.info("")
    logger.info("=" * 70)
    logger.info("🌐 BROWSER IS NOW RUNNING!")
    logger.info("=" * 70)
    logger.info("")
    logger.info("📋 FEATURES AVAILABLE:")
    logger.info("   ✅ All search engines (Google, Brave, DuckDuckGo, etc.)")
    logger.info("   ✅ Privacy logging & bookmarks")
    logger.info("   ✅ Extensions system")
    logger.info("   ✅ Download manager")
    
    if ollama_running and proxy_started:
        logger.info("   ✅ 🤖 AI Chatbot (DeepTalks.ai with Ollama)")
    elif ollama_running:
        logger.info("   ⚠️  🤖 AI Chatbot (limited - CORS proxy failed)")
    else:
        logger.info("   ⚠️  🤖 AI Chatbot (fallback mode - Ollama not running)")
    
    if microservices_ok:
        logger.info("   ✅ 📱 Social Media Quick Tabs (WhatsApp, Instagram, Gmail, Telegram)")
        logger.info("   ✅ 🎭 IP Masking Monitor (4 algorithms)")
        logger.info("   ✅ 🌐 Network Request Interceptor (Ad/tracker blocking)")
        logger.info("   ✅ 🛡️  Security Dashboard (Real-time monitoring)")
    
    logger.info("")
    logger.info("=" * 70)
    logger.info("💡 Press Ctrl+C in terminal to stop browser")
    logger.info("=" * 70)
    logger.info("")
    
    window.showFullScreen()
    window.setGeometry(0, 0, 1280, 720)

    
    # Run the application
    exit_code = app.exec()
    
    logger.info("")
    logger.info("=" * 70)
    logger.info("🛑 Browser closed")
    logger.info(f"Exit code: {exit_code}")
    logger.info(f"🕐 Session ended at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 70)
    
    cleanup_proxy()
    sys.exit(exit_code)

except KeyboardInterrupt:
    logger.warning("\n⚠️  Browser stopped by user (Ctrl+C)")
    cleanup_proxy()
    input("\nPress Enter to exit...")
    sys.exit(0)

except Exception as e:
    logger.error(f"❌ ERROR: Failed to start browser")
    logger.error(f"Error details: {str(e)}")
    logger.exception("Full traceback:")
    print("\n" + "=" * 70)
    print("ERROR OCCURRED!")
    print("=" * 70)
    print(f"Error: {str(e)}")
    print(f"\n📝 Check the log file for details: {log_file}")
    print("=" * 70)
    cleanup_proxy()
    input("\nPress Enter to exit...")
    sys.exit(1)
