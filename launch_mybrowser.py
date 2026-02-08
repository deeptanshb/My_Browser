#!/usr/bin/env python3
"""
My Browser Launcher with Terminal Monitoring and Ollama Integration
Automatically starts the browser and CORS proxy for AI features
"""

import sys
import os
import logging
from datetime import datetime
import subprocess
import time
import signal
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
        logging.StreamHandler(sys.stdout)  # Also print to terminal
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

# Register cleanup function
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
    
    # Check if proxy file exists
    proxy_file = os.path.join(script_dir, 'ollama_cors_proxy.py')
    if not os.path.exists(proxy_file):
        logger.warning("⚠️  ollama_cors_proxy.py not found - AI features may not work")
        return False
    
    try:
        # Start proxy in background
        proxy_log = os.path.join(log_dir, f"proxy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        with open(proxy_log, 'w') as log:
            proxy_process = subprocess.Popen(
                [sys.executable, proxy_file],
                stdout=log,
                stderr=subprocess.STDOUT,
                start_new_session=True
            )
        
        # Wait a moment for proxy to start
        time.sleep(2)
        
        # Check if it's running
        if proxy_process.poll() is None:
            # Verify proxy is accessible
            try:
                import requests
                response = requests.get('http://localhost:8081/api/tags', timeout=2)
                if response.status_code == 200:
                    logger.info(f"✅ CORS proxy started (PID: {proxy_process.pid})")
                    logger.info(f"📝 Proxy log: {proxy_log}")
                    return True
            except:
                pass
        
        logger.warning("⚠️  CORS proxy failed to start - check dependencies")
        proxy_process = None
        return False
        
    except Exception as e:
        logger.warning(f"⚠️  Could not start CORS proxy: {e}")
        proxy_process = None
        return False

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

logger.info("=" * 60)
logger.info("🦕 MY BROWSER LAUNCHER WITH AI")
logger.info("=" * 60)
logger.info(f"Working directory: {os.getcwd()}")
logger.info(f"Log file: {log_file}")
logger.info(f"Starting browser at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

try:
    # Check dependencies
    logger.info("Checking dependencies...")
    missing_deps = check_dependencies()
    
    if missing_deps:
        logger.error(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        print("\n" + "=" * 60)
        print("ERROR: Missing dependencies!")
        print("=" * 60)
        for dep in missing_deps:
            if dep == "PyQt6":
                print("Install PyQt6: sudo apt install python3-pyqt6 python3-pyqt6.qtwebengine")
        print("=" * 60)
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Check Ollama status
    logger.info("")
    logger.info("📡 Checking Ollama status...")
    ollama_running, models = check_ollama_running()
    
    if ollama_running:
        logger.info(f"✅ Ollama is running with {len(models)} model(s)")
        for model in models[:3]:  # Show first 3 models
            logger.info(f"   • {model.get('name', 'unknown')}")
        
        # Start CORS proxy
        logger.info("")
        logger.info("🚀 Starting CORS proxy for AI features...")
        proxy_started = start_cors_proxy()
        
        if proxy_started:
            # Use custom.py (already has CORS fix with port 8080)
            browser_file = 'custom.py'
            logger.info("✅ Using custom.py with CORS fix")
        else:
            browser_file = 'custom.py'
    else:
        logger.warning("⚠️  Ollama not running")
        logger.info("   AI chatbot will be in fallback mode")
        logger.info("   To enable AI: run 'ollama serve' in another terminal")
        browser_file = 'custom.py'
    
    logger.info("")
    logger.info("Loading browser modules...")
    
    # Import PyQt6
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QFont
    logger.info("✅ PyQt6 loaded")
    
    # Import browser
    logger.info(f"Importing browser from custom.py...")
    from custom import ModernBrowser
    
    logger.info("Initializing Qt Application...")
    app = QApplication(sys.argv)
    app.setApplicationName("My Browser - Custom Design")
    app.setOrganizationName("MyBrowser")
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    logger.info("Creating browser window...")
    window = ModernBrowser()
    
    logger.info("✅ Browser successfully initialized!")
    logger.info("🌐 Opening browser window...")
    window.show()
    
    logger.info("")
    logger.info("🦕 Browser is now running!")
    if ollama_running and proxy_process:
        logger.info("🤖 AI chatbot ready with Ollama integration")
    logger.info("=" * 60)
    logger.info("MONITORING ACTIVE - Press Ctrl+C in terminal to stop")
    logger.info("=" * 60)
    
    # Run the application
    exit_code = app.exec()
    
    logger.info("=" * 60)
    logger.info("🛑 Browser closed")
    logger.info(f"Exit code: {exit_code}")
    logger.info(f"Session ended at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
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
    print("\n" + "=" * 60)
    print("ERROR OCCURRED!")
    print("=" * 60)
    print(f"Error: {str(e)}")
    print(f"\nCheck the log file for details: {log_file}")
    print("=" * 60)
    cleanup_proxy()
    input("\nPress Enter to exit...")
    sys.exit(1)