"""
Custom Multi-Engine Browser - Advanced Privacy Features
With VPN proxy, secure DNS, search logging, and extensions support\n"""
import sys
import json
import os
from datetime import datetime
from PyQt6.QtCore import QUrl, Qt, QSize, QTimer
from PyQt6.QtNetwork import QNetworkProxy
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLineEdit, 
    QTabWidget, QWidget, QVBoxLayout, QStatusBar, QHBoxLayout,
    QDialog, QListWidget, QPushButton, QLabel, QFileDialog,
    QMenu, QMessageBox, QInputDialog, QComboBox, QFrame, QCheckBox,
    QTextEdit, QGroupBox, QRadioButton, QSpinBox
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import (
    QWebEngineProfile, QWebEngineDownloadRequest,
    QWebEnginePage, QWebEngineSettings, QWebEngineScript
)
from PyQt6.QtGui import QAction, QKeySequence, QIcon, QFont
from PyQt6.QtNetwork import QNetworkProxy as QNetProxy

import sys
import os

# Optional microservices
try:
    _mod_path = os.path.join(os.path.dirname(__file__), 'modules')
    if _mod_path not in sys.path:
        sys.path.insert(0, _mod_path)
    from network_interceptor import NetworkRequestInterceptor
    from security_monitor import SecurityMonitor
    MODULES_AVAILABLE = True
except:
    MODULES_AVAILABLE = False
    NetworkRequestInterceptor = None
    SecurityMonitor = None



# ── MICROSERVICES ──────────────────────────────────────────────
import socket as _socket_mod
import hashlib as _hashlib_mod
import struct as _struct_mod
import random as _random_mod
import threading as _threading_mod

_ms_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules')
if _ms_dir not in sys.path:
    sys.path.insert(0, _ms_dir)

try:
    from modules.network_interceptor import NetworkRequestInterceptor
    from modules.ip_masking import IPMaskingMonitor
    from modules.social_tabs import SocialTabManager
    from modules.security_monitor import SecurityMonitor
    MODULES_AVAILABLE = True
    print("✓ Microservices modules loaded")
except ImportError as e:
    MODULES_AVAILABLE = False
    print(f"⚠  Microservices not loaded: {e}")
# ──────────────────────────────────────────────────────────────

# Search Engine Configuration - BROWSERS (what user sees)
BROWSERS = {
    'My Browser': {
        'url': 'about:home',
        'search_url': 'BACKEND',  # Will use backend_search_engine from settings
        'icon': '🦕',
        'color': '#6366F1',
        'gradient_start': '#667eea',
        'gradient_end': '#764ba2',
        'description': 'Your custom search experience',
        'theme': 'custom'
    },
    'Google': {
        'url': 'https://www.google.com',
        'search_url': 'https://www.google.com/search?q={}',
        'icon': '🔍',
        'color': '#4285F4',
        'gradient_start': '#4285F4',
        'gradient_end': '#34A853',
        'description': 'Most comprehensive results',
        'theme': 'google'
    },
    'Brave': {
        'url': 'https://search.brave.com',
        'search_url': 'https://search.brave.com/search?q={}',
        'icon': '🦁',
        'color': '#FB542B',
        'gradient_start': '#FB542B',
        'gradient_end': '#FFA500',
        'description': 'Private & ad-free search',
        'theme': 'brave'
    },
    'DuckDuckGo': {
        'url': 'https://duckduckgo.com',
        'search_url': 'https://duckduckgo.com/?q={}',
        'icon': '🦆',
        'color': '#DE5833',
        'gradient_start': '#DE5833',
        'gradient_end': '#66B032',
        'description': 'Privacy-focused search',
        'theme': 'duckduckgo'
    }
}

# BACKEND SEARCH ENGINES (what My Browser uses internally)
SEARCH_ENGINES = {
    'Brave Search': {
        'search_url': 'https://search.brave.com/search?q={}',
        'icon': '🦁',
        'description': 'Private & ad-free'
    },
    'Google': {
        'search_url': 'https://www.google.com/search?q={}',
        'icon': '🔍',
        'description': 'Most comprehensive'
    },
    'DuckDuckGo': {
        'search_url': 'https://duckduckgo.com/?q={}',
        'icon': '🦆',
        'description': 'Privacy-focused'
    },
    'Bing': {
        'search_url': 'https://www.bing.com/search?q={}',
        'icon': '🅱️',
        'description': 'Microsoft search'
    },
    'Yahoo': {
        'search_url': 'https://search.yahoo.com/search?p={}',
        'icon': '🟣',
        'description': 'Classic portal'
    },
    'Ecosia': {
        'search_url': 'https://www.ecosia.org/search?q={}',
        'icon': '🌳',
        'description': 'Plant trees'
    },
    'Startpage': {
        'search_url': 'https://www.startpage.com/do/search?q={}',
        'icon': '🔐',
        'description': 'Private Google'
    },
    'Qwant': {
        'search_url': 'https://www.qwant.com/?q={}',
        'icon': '🔵',
        'description': 'French privacy'
    },
    'Yandex': {
        'search_url': 'https://yandex.com/search/?text={}',
        'icon': '🔴',
        'description': 'Russian search'
    },
    'Searx': {
        'search_url': 'https://searx.be/search?q={}',
        'icon': '🔎',
        'description': 'Metasearch'
    },
    'Wikipedia': {
        'search_url': 'https://en.wikipedia.org/wiki/Special:Search?search={}',
        'icon': '📚',
        'description': 'Encyclopedia'
    },
    'YouTube': {
        'search_url': 'https://www.youtube.com/results?search_query={}',
        'icon': '📺',
        'description': 'Video search'
    },
    'GitHub': {
        'search_url': 'https://github.com/search?q={}',
        'icon': '🐙',
        'description': 'Code search'
    },
}

# Secure DNS Servers
DNS_SERVERS = {
    'Cloudflare': {'primary': '1.1.1.1', 'secondary': '1.0.0.1', 'description': 'Fast & Private'},
    'Google': {'primary': '8.8.8.8', 'secondary': '8.8.4.4', 'description': 'Reliable & Fast'},
    'Quad9': {'primary': '9.9.9.9', 'secondary': '149.112.112.112', 'description': 'Security Focused'},
    'OpenDNS': {'primary': '208.67.222.222', 'secondary': '208.67.220.220', 'description': 'Family Safe'},
}

# Free VPN/Proxy servers (for demonstration - you should use proper VPN service)
PROXY_SERVERS = {
    'None': {'host': '', 'port': 0, 'type': 'none'},
    'Custom': {'host': '', 'port': 0, 'type': 'http'},
}

DEFAULT_BROWSER = 'My Browser'
DEFAULT_SEARCH_ENGINE = 'My Browser'  # Default search engine for startup


class PrivacyLogger:
    """Log all searches and browsing for privacy auditing"""
    
    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.search_log_file = os.path.join(log_dir, "search_log.txt")
        self.privacy_log_file = os.path.join(log_dir, "privacy_log.json")
        
    def log_search(self, query, engine, timestamp=None):
        """Log a search query"""
        try:
            if not query or not query.strip():
                return
            if timestamp is None:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            os.makedirs(self.log_dir, exist_ok=True)
            try:
                with open(self.search_log_file, 'a', encoding='utf-8') as f:
                    f.write(f"[{timestamp}] Engine: {engine} | Query: {query}\n")
            except Exception:
                pass
            try:
                if os.path.exists(self.privacy_log_file):
                    with open(self.privacy_log_file, 'r', encoding='utf-8') as f:
                        logs = json.load(f)
                else:
                    logs = []
            except Exception:
                logs = []
            logs.append({'timestamp': timestamp, 'type': 'search', 'engine': engine, 'query': query})
            if len(logs) > 10000:
                logs = logs[-10000:]
            with open(self.privacy_log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2)
        except Exception:
            pass
    
    def log_page_visit(self, url, title=""):
        """Log a page visit"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            if os.path.exists(self.privacy_log_file):
                with open(self.privacy_log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
        except:
            logs = []
        
        logs.append({
            'timestamp': timestamp,
            'type': 'visit',
            'url': url,
            'title': title
        })
        
        # Keep only last 10000 entries
        if len(logs) > 10000:
            logs = logs[-10000:]
        
        with open(self.privacy_log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2)
    
    def get_search_history(self, limit=100):
        """Get recent search history"""
        try:
            if os.path.exists(self.privacy_log_file):
                with open(self.privacy_log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                    searches = [log for log in logs if log['type'] == 'search']
                    return searches[-limit:]
        except:
            pass
        return []


class ExtensionManager:
    """Manage browser extensions (custom scripts)"""
    
    def __init__(self, extension_dir):
        self.extension_dir = extension_dir
        os.makedirs(extension_dir, exist_ok=True)
        self.extensions = self.load_extensions()
    
    def load_extensions(self):
        """Load all extensions from directory"""
        extensions = []
        
        # Load built-in extensions
        extensions.extend(self.get_builtin_extensions())
        
        # Load user extensions
        for filename in os.listdir(self.extension_dir):
            if filename.endswith('.js'):
                filepath = os.path.join(self.extension_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        code = f.read()
                        extensions.append({
                            'name': filename[:-3],
                            'code': code,
                            'enabled': True,
                            'builtin': False
                        })
                except:
                    pass
        
        return extensions
    
    def get_builtin_extensions(self):
        """Get built-in extensions"""
        return [
            {
                'name': 'Light Mode Enforcer',
                'code': '''
                    // Force light mode on all websites by default
                    (function() {
                        // Skip My Browser custom pages
                        if (window.location.href.startsWith('data:') || 
                            window.location.href.startsWith('about:')) {
                            return;
                        }
                        
                        // Force light mode by setting color scheme
                        const style = document.createElement('style');
                        style.id = 'mybrowser-force-light';
                        style.textContent = `
                            :root {
                                color-scheme: light !important;
                            }
                            body, html {
                                background-color: white !important;
                                color: black !important;
                            }
                        `;
                        document.head.appendChild(style);
                        
                        // Override prefers-color-scheme
                        if (window.matchMedia) {
                            const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
                            Object.defineProperty(darkModeQuery, 'matches', {
                                get: () => false
                            });
                        }
                    })();
                ''',
                'enabled': True,
                'builtin': True
            },
            {
                'name': 'Ad Blocker',
                'code': '''
                    // Hide common ad elements
                    (function() {
                        const adSelectors = [
                            '.ad', '.ads', '.advertisement', 
                            '[class*="adsbygoogle"]', '[id*="google_ads"]',
                            '[class*="ad-container"]', '[class*="sponsored"]',
                            '.banner-ad', '[id*="ad-"]'
                        ];
                        
                        function hideAds() {
                            adSelectors.forEach(selector => {
                                document.querySelectorAll(selector).forEach(el => {
                                    el.style.display = 'none';
                                });
                            });
                        }
                        
                        hideAds();
                        setInterval(hideAds, 1000);
                    })();
                ''',
                'enabled': True,
                'builtin': True
            },
            {
                'name': 'Dark Mode',
                'code': '''
                    // Smart dark mode - UI elements for My Browser, full invert for other sites
                    (function() {
                        // Check if dark mode style already exists
                        if (document.getElementById('mybrowser-darkmode')) {
                            return; // Already applied
                        }
                        
                        // Create dark mode style
                        const style = document.createElement('style');
                        style.id = 'mybrowser-darkmode';
                        
                        // Check if this is My Browser custom page
                        const isMyBrowserPage = window.location.href.startsWith('data:') || 
                                               window.location.href.startsWith('about:');
                        
                        if (isMyBrowserPage) {
                            // For My Browser: Only darken UI elements, keep gradient background
                            style.textContent = `
                                /* Keep the gradient background beautiful */
                                body, html {
                                    /* Background stays as is - no filter on body */
                                }
                                
                                /* Darken the search bar */
                                .search-wrapper {
                                    background: rgba(30, 30, 40, 0.95) !important;
                                    border: 2px solid rgba(255, 255, 255, 0.1) !important;
                                }
                                
                                #searchInput {
                                    background: rgba(40, 40, 50, 0.8) !important;
                                    color: #ffffff !important;
                                }
                                
                                #searchInput::placeholder {
                                    color: rgba(255, 255, 255, 0.5) !important;
                                }
                                
                                /* Darken text elements */
                                h1, .subtitle, .time, .date {
                                    color: #e0e0e0 !important;
                                    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5) !important;
                                }
                                
                                /* Darken quick links */
                                .quick-link {
                                    background: rgba(30, 30, 40, 0.7) !important;
                                    border: 1px solid rgba(255, 255, 255, 0.2) !important;
                                    color: #e0e0e0 !important;
                                }
                                
                                .quick-link:hover {
                                    background: rgba(50, 50, 60, 0.8) !important;
                                }
                                
                                /* Darken privacy badge */
                                .privacy-badge {
                                    background: rgba(30, 40, 30, 0.8) !important;
                                    border: 1px solid rgba(76, 175, 80, 0.5) !important;
                                }
                                
                                /* Darken any other UI elements */
                                .container {
                                    background: rgba(0, 0, 0, 0.1) !important;
                                    border-radius: 20px;
                                }
                            `;
                        } else {
                            // For external websites: Full dark mode with invert
                            style.textContent = `
                                html {
                                    filter: invert(0.9) hue-rotate(180deg) !important;
                                    background-color: #1a1a1a !important;
                                }
                                img, video, [style*="background-image"], 
                                picture, canvas, iframe, svg {
                                    filter: invert(1) hue-rotate(180deg) !important;
                                }
                            `;
                        }
                        
                        document.head.appendChild(style);
                    })();
                ''',
                'enabled': False,
                'builtin': True
            },
            {
                'name': 'Auto Scroll',
                'code': '''
                    // Auto scroll with arrow keys
                    (function() {
                        let scrolling = false;
                        
                        document.addEventListener('keydown', (e) => {
                            if (e.key === 'ArrowDown') {
                                window.scrollBy(0, 100);
                            } else if (e.key === 'ArrowUp') {
                                window.scrollBy(0, -100);
                            }
                        });
                    })();
                ''',
                'enabled': False,
                'builtin': True
            },
            {
                'name': 'Privacy Shield',
                'code': '''
                    // Block trackers and fingerprinting
                    (function() {
                        // Override navigator properties for privacy
                        Object.defineProperty(navigator, 'webdriver', {get: () => false});
                        
                        // Block common trackers
                        const blockedDomains = ['google-analytics.com', 'doubleclick.net', 'facebook.net'];
                        
                        const originalFetch = window.fetch;
                        window.fetch = function(...args) {
                            const url = args[0];
                            if (blockedDomains.some(domain => url.includes(domain))) {
                                console.log('Blocked tracker:', url);
                                return Promise.reject(new Error('Blocked by Privacy Shield'));
                            }
                            return originalFetch.apply(this, args);
                        };
                    })();
                ''',
                'enabled': True,
                'builtin': True
            }
        ]
    
    def get_enabled_scripts(self):
        """Get all enabled extension scripts"""
        return [ext['code'] for ext in self.extensions if ext['enabled']]
    
    def toggle_extension(self, name):
        """Toggle extension on/off"""
        for ext in self.extensions:
            if ext['name'] == name:
                ext['enabled'] = not ext['enabled']
                return ext['enabled']
        return False


class CustomSearchPage:
    """Custom search page HTML generator"""
    
    @staticmethod
    def get_html():
        return r"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>My Browser - Search</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    position: relative;
                    overflow-x: hidden;
                }
                .background { position: fixed; width: 100%; height: 100%; top: 0; left: 0; z-index: 0; }
                .stars { position: absolute; width: 100%; height: 100%; overflow: hidden; }
                .star { position: absolute; width: 2px; height: 2px; background: white; border-radius: 50%; animation: twinkle 3s infinite; }
                @keyframes twinkle { 0%, 100% { opacity: 0; } 50% { opacity: 1; } }
                .container { position: relative; z-index: 10; text-align: center; padding: 2rem; max-width: 900px; width: 100%; }
                .logo { font-size: 6rem; margin-bottom: 1rem; animation: float 3s ease-in-out infinite; filter: drop-shadow(0 10px 20px rgba(0,0,0,0.3)); }
                @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
                h1 { color: white; font-size: 4rem; font-weight: 700; text-shadow: 0 4px 6px rgba(0,0,0,0.2); }
                .subtitle { color: rgba(255, 255, 255, 0.95); font-size: 1.4rem; margin-bottom: 3rem; font-weight: 300; }
                .search-container { margin: 3rem auto; max-width: 700px; }
                .search-wrapper { position: relative; background: rgba(255, 255, 255, 0.95); border-radius: 50px; padding: 8px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); transition: all 0.3s; }
                .search-wrapper:hover { background: white; box-shadow: 0 15px 50px rgba(0,0,0,0.4); transform: translateY(-2px); }
                .search-icon { position: absolute; left: 25px; top: 50%; transform: translateY(-50%); font-size: 1.5rem; color: #667eea; }
                #searchInput { width: 100%; padding: 18px 60px; border: none; background: transparent; font-size: 1.1rem; color: #1a1a2e; outline: none; font-weight: 500; }
                .time { font-size: 3.5rem; color: white; font-weight: 200; margin-top: 2rem; text-shadow: 0 2px 10px rgba(0,0,0,0.2); }
                .date { font-size: 1.3rem; color: rgba(255, 255, 255, 0.9); margin-bottom: 2rem; }
                .quick-links { display: flex; justify-content: center; gap: 1rem; margin-top: 2rem; flex-wrap: wrap; }
                .quick-link { background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px; padding: 1rem 1.5rem; color: white; font-weight: 500; cursor: pointer; transition: all 0.3s; }
                .quick-link:hover { background: rgba(255, 255, 255, 0.25); transform: translateY(-3px); }
                .privacy-badge { background: rgba(76, 175, 80, 0.3); padding: 0.5rem 1rem; border-radius: 10px; color: white; margin-top: 2rem; display: inline-block; }
                
                /* DeepTalks.AI Chatbot Styles */
                .chatbot-container {
                    position: fixed;
                    bottom: 30px;
                    right: 30px;
                    z-index: 1000;
                }
                
                .chatbot-toggle {
                    width: 200px;
                    height: 65px;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    border-radius: 33px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5);
                    transition: all 0.3s ease;
                    animation: pulse 2s infinite;
                    border: 3px solid rgba(255,255,255,0.3);
                    position: relative;
                    overflow: hidden;
                }
                
                .chatbot-toggle::before {
                    content: '';
                    position: absolute;
                    top: -50%;
                    left: -50%;
                    width: 200%;
                    height: 200%;
                    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
                    animation: shine 3s infinite;
                }
                
                @keyframes pulse {
                    0%, 100% { box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5); }
                    50% { box-shadow: 0 12px 45px rgba(102, 126, 234, 0.7); }
                }
                
                @keyframes shine {
                    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
                    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
                }
                
                .chatbot-toggle:hover {
                    transform: scale(1.08);
                    box-shadow: 0 12px 40px rgba(102, 126, 234, 0.7);
                }
                
                .chatbot-toggle-icon {
                    font-size: 30px;
                    margin-right: 10px;
                    z-index: 1;
                }
                
                .chatbot-toggle-text {
                    color: white;
                    font-weight: bold;
                    font-size: 17px;
                    letter-spacing: 0.5px;
                    z-index: 1;
                }
                
                .ai-badge {
                    position: absolute;
                    top: 5px;
                    right: 10px;
                    background: rgba(255,255,255,0.3);
                    color: white;
                    padding: 2px 8px;
                    border-radius: 10px;
                    font-size: 10px;
                    font-weight: bold;
                    z-index: 1;
                }
                
                .chatbot-window {
                    position: fixed;
                    bottom: 110px;
                    right: 30px;
                    width: 420px;
                    height: 650px;
                    background: white;
                    border-radius: 25px;
                    box-shadow: 0 20px 80px rgba(0,0,0,0.4);
                    display: none;
                    flex-direction: column;
                    overflow: hidden;
                    animation: slideInUp 0.4s ease-out;
                    border: 3px solid rgba(102, 126, 234, 0.3);
                }
                
                @keyframes slideInUp {
                    from { transform: translateY(100%); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }
                
                .chatbot-window.active {
                    display: flex;
                }
                
                .chatbot-header {
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    padding: 25px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                }
                
                .chatbot-title {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    flex-direction: column;
                    align-items: flex-start;
                }
                
                .chatbot-title-main {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
                
                .chatbot-title-icon { font-size: 26px; }
                .chatbot-title-text { font-weight: bold; font-size: 20px; }
                
                .chatbot-subtitle {
                    font-size: 11px;
                    opacity: 0.9;
                    font-weight: normal;
                    margin-left: 36px;
                }
                
                .chatbot-close {
                    background: rgba(255,255,255,0.2);
                    border: none;
                    color: white;
                    width: 35px;
                    height: 35px;
                    border-radius: 50%;
                    cursor: pointer;
                    font-size: 20px;
                    transition: all 0.3s ease;
                }
                
                .chatbot-close:hover {
                    background: rgba(255,255,255,0.3);
                    transform: rotate(90deg);
                }
                
                .chatbot-messages {
                    flex: 1;
                    overflow-y: auto;
                    padding: 25px;
                    background: #f8f9fa;
                }
                
                .message {
                    margin-bottom: 18px;
                    display: flex;
                    animation: fadeIn 0.3s ease-out;
                }
                
                .message.user { justify-content: flex-end; }
                
                .message-content {
                    max-width: 80%;
                    padding: 14px 20px;
                    border-radius: 20px;
                    word-wrap: break-word;
                    line-height: 1.5;
                }
                
                .message.bot .message-content {
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    border-bottom-left-radius: 6px;
                    box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
                }
                
                .message.user .message-content {
                    background: #e9ecef;
                    color: #333;
                    border-bottom-right-radius: 6px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }
                
                /* Code block styling */
                .message-content pre {
                    background: rgba(0, 0, 0, 0.2);
                    border-radius: 8px;
                    padding: 15px;
                    margin: 10px 0;
                    overflow-x: auto;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }
                
                .message-content code {
                    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                    font-size: 13px;
                    line-height: 1.6;
                }
                
                .message-content pre code {
                    display: block;
                    background: transparent;
                    padding: 0;
                    color: #fff;
                    white-space: pre;
                    word-wrap: normal;
                }
                
                .message-content :not(pre) > code {
                    background: rgba(0, 0, 0, 0.2);
                    padding: 3px 7px;
                    border-radius: 4px;
                    font-size: 12px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }
                
                .message.user .message-content pre {
                    background: rgba(0, 0, 0, 0.08);
                    border: 1px solid rgba(0, 0, 0, 0.1);
                }
                
                .message.user .message-content pre code {
                    color: #2d3748;
                }
                
                .message.user .message-content :not(pre) > code {
                    background: rgba(0, 0, 0, 0.1);
                    border: 1px solid rgba(0, 0, 0, 0.15);
                }
                
                .chatbot-input-area {
                    padding: 20px;
                    background: white;
                    border-top: 2px solid #e9ecef;
                    display: flex;
                    gap: 12px;
                }
                
                .chatbot-input {
                    flex: 1;
                    padding: 14px 20px;
                    border: 2px solid #e9ecef;
                    border-radius: 25px;
                    outline: none;
                    font-size: 15px;
                    transition: all 0.3s ease;
                }
                
                .chatbot-input:focus {
                    border-color: #667eea;
                    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
                }
                
                .chatbot-send {
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    border: none;
                    width: 50px;
                    height: 50px;
                    border-radius: 50%;
                    cursor: pointer;
                    font-size: 22px;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                }
                
                .chatbot-send:hover {
                    transform: scale(1.1);
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
                }
                
                .chatbot-send:disabled {
                    opacity: 0.5;
                    cursor: not-allowed;
                }
                
                .typing-indicator {
                    display: flex;
                    gap: 6px;
                    padding: 14px 20px;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    border-radius: 20px;
                    border-bottom-left-radius: 6px;
                    max-width: 80px;
                }
                
                .typing-dot {
                    width: 9px;
                    height: 9px;
                    background: white;
                    border-radius: 50%;
                    animation: typingAnimation 1.4s infinite;
                }
                
                .typing-dot:nth-child(2) { animation-delay: 0.2s; }
                .typing-dot:nth-child(3) { animation-delay: 0.4s; }
                
                @keyframes typingAnimation {
                    0%, 60%, 100% { transform: translateY(0); }
                    30% { transform: translateY(-12px); }
                }
                
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                
                .model-indicator {
                    text-align: center;
                    padding: 10px;
                    background: rgba(102, 126, 234, 0.1);
                    font-size: 12px;
                    color: #667eea;
                    font-weight: 600;
                }
                
                @media (max-width: 768px) {
                    .chatbot-window {
                        width: calc(100vw - 40px);
                        right: 20px;
                        bottom: 100px;
                    }
                    .chatbot-container { right: 20px; }
                }
            </style>
        </head>
        <body>
            <div class="background"><div class="stars" id="stars"></div></div>
            <div class="container">
                <div class="logo">🦕</div>
                <h1>My Browser</h1>
                <p class="subtitle">🔒 Private & Secure Browsing</p>
                <div class="search-container">
                    <div class="search-wrapper">
                        <span class="search-icon">🔍</span>
                        <input type="text" id="searchInput" placeholder="Search privately or enter URL..." autocomplete="off" />
                    </div>
                </div>
                <div class="time" id="time">00:00</div>
                <div class="date" id="date">Loading...</div>
                <div class="quick-links">
                    <div class="quick-link" onclick="performSearch('news')">📰 News</div>
                    <div class="quick-link" onclick="performSearch('weather')">🌤️ Weather</div>
                    <div class="quick-link" onclick="performSearch('videos')">🎬 Videos</div>
                    <div class="quick-link" onclick="performSearch('images')">🖼️ Images</div>
                </div>
                <div class="privacy-badge">🛡️ DNS Protected • Search Logged • Extensions Active</div>
            </div>
            
            <!-- DeepTalks.AI Chatbot -->
            <div class="chatbot-container">
                <div class="chatbot-toggle" onclick="toggleChatbot()">
                    <span class="ai-badge">AI</span>
                    <span class="chatbot-toggle-icon">🦜</span>
                    <span class="chatbot-toggle-text">deeptalks.ai</span>
                </div>
                
                <div class="chatbot-window" id="chatbotWindow">
                    <div class="chatbot-header">
                        <div class="chatbot-title">
                            <div class="chatbot-title-main">
                                <span class="chatbot-title-icon">🦜</span>
                                <span class="chatbot-title-text">deeptalks.ai</span>
                            </div>
                            <span class="chatbot-subtitle">Powered by Open Source LLM</span>
                        </div>
                        <button class="chatbot-close" onclick="toggleChatbot()">×</button>
                    </div>
                    
                    <div class="model-indicator" id="modelIndicator">
                        🔄 Connecting to AI Model...
                    </div>
                    
                    <div class="chatbot-messages" id="chatMessages">
                        <div class="message bot">
                            <div class="message-content">
                                👋 Hello! I am DeepTalks.AI, powered by real AI. I can help you with questions, creative writing, coding, analysis, and much more. I also have web search enabled for current news and real-time information! What would you like to talk about?
                            </div>
                        </div>
                    </div>
                    
                    <!-- Attach preview (filled by Python via runJavaScript) -->
                    <div id="attachPreview" style="display:none;padding:8px 14px;background:rgba(116,192,252,0.08);border-top:1px solid rgba(116,192,252,0.2);font-size:12px;color:#ccc;align-items:center;gap:8px;border-left:3px solid #74c0fc;"></div>
                    
                    <!-- Attach toolbar - visible buttons that call Python -->
                    <div style="padding:6px 14px;display:flex;align-items:center;gap:8px;border-top:1px solid rgba(255,255,255,0.08);background:rgba(255,255,255,0.03);">
                        <button onclick="window.pythonAttachImage()" title="Attach image" 
                                style="background:rgba(116,192,252,0.15);border:1px solid rgba(116,192,252,0.3);color:#74c0fc;border-radius:6px;padding:6px 12px;cursor:pointer;font-size:14px;display:flex;align-items:center;gap:4px;">
                            🖼️ <span style="font-size:12px;">Image</span>
                        </button>
                        <button onclick="window.pythonAttachFile()" title="Attach file (.txt .py .md .csv etc)" 
                                style="background:rgba(116,192,252,0.15);border:1px solid rgba(116,192,252,0.3);color:#74c0fc;border-radius:6px;padding:6px 12px;cursor:pointer;font-size:14px;display:flex;align-items:center;gap:4px;">
                            📎 <span style="font-size:12px;">File</span>
                        </button>
                        <div style="flex:1;"></div>
                        <label style="display:flex;align-items:center;gap:5px;cursor:pointer;font-size:11px;color:#999;">
                            <input type="checkbox" id="webSearchToggle" checked style="cursor:pointer;accent-color:#667eea;">
                            🔍 Web search
                        </label>
                    </div>
                    <div id="searchStatus" style="padding:2px 14px;font-size:10px;color:#666;font-style:italic;min-height:14px;"></div>
                    
                    <!-- Input row -->
                    <div class="chatbot-input-area">
                        <input type="text" class="chatbot-input" id="chatInput"
                               placeholder="Ask anything…"
                               onkeypress="handleChatKeyPress(event)">
                        <button class="chatbot-send" id="sendBtn" onclick="sendMessage()">➤</button>
                    </div>
                </div>
            </div>
            <script>
                for (let i = 0; i < 150; i++) {
                    const star = document.createElement('div');
                    star.className = 'star';
                    star.style.left = Math.random() * 100 + '%';
                    star.style.top = Math.random() * 100 + '%';
                    star.style.animationDelay = Math.random() * 3 + 's';
                    document.getElementById('stars').appendChild(star);
                }
                function updateTime() {
                    const now = new Date();
                    document.getElementById('time').textContent = now.toTimeString().slice(0,5);
                    document.getElementById('date').textContent = now.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
                }
                updateTime();
                setInterval(updateTime, 1000);
                
                document.getElementById('searchInput').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') performSearch(this.value);
                });
                
                function performSearch(query) {
                    if (!query || query.trim() === '') return;
                    if (query.includes('.') && !query.includes(' ')) {
                        window.location.href = query.startsWith('http') ? query : 'http://' + query;
                    } else {
                        window.location.href = 'https://search.brave.com/search?q=' + encodeURIComponent(query);
                    }
                }
                
                document.getElementById('searchInput').focus();
                
                /* ================================
                   DeepTalks.AI – ENHANCED: Web Search + File/Image + Sources
                   ================================================================ */

                let chatbotOpen = false;
                let conversationHistory = [];
                let currentModel = null;
                let ollamaActive = false;
                let attachedFile = null;

                /* ── Ollama detection ─────────────────────────── */
                async function checkOllamaConnection() {
                    try {
                        const r = await fetch('http://localhost:8081/api/tags');
                        if (!r.ok) throw new Error();
                        const d = await r.json();
                        if (d.models && d.models.length > 0) {
                            currentModel = d.models[0].name;
                            ollamaActive = true;
                            updateModelIndicator('✓ Connected: ' + currentModel);
                            return true;
                        }
                    } catch {}
                    ollamaActive = false; currentModel = null;
                    updateModelIndicator('⚠️ Ollama not running – Limited mode');
                    return false;
                }

                function updateModelIndicator(text) {

                    document.getElementById('modelIndicator').textContent = text;
                }

                function toggleChatbot() {
                    const win = document.getElementById('chatbotWindow');
                    chatbotOpen = !chatbotOpen;
                    if (chatbotOpen) {
                        win.classList.add('active');
                        document.getElementById('chatInput').focus();
                        checkOllamaConnection();
                    } else { win.classList.remove('active'); }
                }
                // ── Python attach button wiring ───────────────────────
                // These get called by the 🖼️ and 📎 buttons inside the chat window
                // They trigger the Python _chat_attach_* methods via a simple mechanism:
                // Instead of complex QWebChannel, we just set a flag and poll it from Python
                window._attachImageRequested = false;
                window._attachFileRequested = false;
                
                window.pythonAttachImage = function() {
                    console.log('[chatbot] 🖼️ Image attach requested');
                    window._attachImageRequested = true;
                    // Python will poll this flag via setInterval in _run_chat_js
                };
                window.pythonAttachFile = function() {
                    console.log('[chatbot] 📎 File attach requested');
                    window._attachFileRequested = true;
                };

                

                function handleChatKeyPress(e) {
                    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
                }

                /* ── Attachment (managed by Python via runJavaScript) ── */
                // File/image picking is done in Python using QFileDialog.
                // Python calls page().runJavaScript() to set window.attachedFile
                // and show the preview banner. No JS file-input needed here.
                function showAttachPreview(text) {


                    const p = document.getElementById('attachPreview');
                    if (!p) return;

                    p.style.display = 'flex';
                    p.innerHTML = '<span>' + text + '</span>' +
                        '<button id="removeAttachBtn" ' +
                        'style="margin-left:auto;background:none;border:none;color:#ff6b6b;cursor:pointer;font-size:14px;">✕</button>';

                    document.getElementById('removeAttachBtn').onclick = function() {
                        window.attachedFile = null;
                        window._attachedFile = null;
                        p.style.display = 'none';
                    };
                }   


                /* ── Send message ─────────────────────────────── */
                async function sendMessage() {
                    const input = document.getElementById('chatInput');
                    const message = input.value.trim();
                    // Read from window.attachedFile — set by Python via runJavaScript()
                    const attach = window.attachedFile || null;
                    if (!message && !attach) return;

                    let userDisplay = escapeHtml(message || '');
                    if (attach) {
                        if (attach.type === 'image' && attach.dataUrl) {
                            userDisplay += '<br><img src="' + attach.dataUrl
                                + '" style="max-width:180px;max-height:130px;border-radius:6px;margin-top:5px;">';
                        } else {
                            userDisplay += '<br><small>📎 ' + escapeHtml(attach.name) + '</small>';
                        }
                    }
                    addRawMessage(userDisplay, 'user');
                    conversationHistory.push({ role: 'user', content: message || '[attachment]' });
                    input.value = '';
                    document.getElementById('sendBtn').disabled = true;
                    showTypingIndicator();

                    try {
                        if (!ollamaActive) await checkOllamaConnection();
                        const { reply, sources } = await getAIResponse(message, attach);
                        addBotMessage(reply, sources);
                        conversationHistory.push({ role: 'assistant', content: reply });
                    } catch(err) {
                        addBotMessage('⚠️ Error: ' + err.message, []);
                    }
                    // Clear attach
                    window.attachedFile = null;
                    window._attachedFile = null;
                    const p = document.getElementById('attachPreview');
                    if (p) { p.style.display = 'none'; p.innerHTML = ''; }
                    hideTypingIndicator();
                    document.getElementById('sendBtn').disabled = false;
                }

                /* ── Web search ───────────────────────────────── */
                function requiresWebSearch(msg) {
                    if (!document.getElementById('webSearchToggle').checked) return false;
                    const kw = ['news','current','latest','today','recent','2025','2026',
                        'weather','stock','price','what happened','breaking','who is',
                        'search for','look up','tell me about','find out'];
                    return kw.some(k => msg.toLowerCase().includes(k));
                }

                async function performWebSearch(query) {
                    const st = document.getElementById('searchStatus');
                    st.textContent = '🔍 Searching…';
                    try {
                        // Route through localhost:8081/search (same origin as Ollama proxy)
                        // This avoids CORS issues with setHtml() null origin
                        const r = await fetch('http://localhost:8081/search?q='
                            + encodeURIComponent(query), { method: 'GET' });
                        if (!r.ok) throw new Error('search failed');
                        const data = await r.json();
                        st.textContent = data.sources && data.sources.length
                            ? '✅ ' + data.sources.length + ' sources found'
                            : data.text ? '✅ Result found' : '';
                        return {
                            text: data.text || null,
                            sources: data.sources || []
                        };
                    } catch(e) {
                        st.textContent = '⚠️ Search unavailable';
                        console.warn('[search]', e);
                        return { text: null, sources: [] };
                    }
                }

                /* ── AI response ──────────────────────────────── */
                async function getAIResponse(userMessage, attach) {
                    let context = ''; let sources = [];

                    if (attach) {
                        if (attach.type === 'file' && attach.content) {
                            context += '\n[Attached file: ' + attach.name + ']\n'
                                + attach.content.slice(0, 4000) + '\n[End file]\nUser question: ';
                        } else if (attach.type === 'image') {
                            context += '\n[User attached image: ' + attach.name
                                + '. Acknowledge it and help.]\n';
                        }
                    }

                    if (userMessage && requiresWebSearch(userMessage)) {
                        const res = await performWebSearch(userMessage);
                        if (res.text) {
                            context += '\n[Web search results]\n' + res.text + '\n[Answer based on above]\n';
                            sources = res.sources;
                        }
                    }

                    const prompt = context + (userMessage || '');
                    if (ollamaActive) {
                        try {
                            const r = await fetch('http://localhost:8081/api/generate', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    model: currentModel || 'mistral:latest',
                                    prompt: prompt, stream: false,
                                    system: 'You are DeepTalks.AI. Use web search results when provided. Analyse files carefully. Format code in triple-backtick blocks.'
                                })
                            });
                            if (r.ok) {
                                const d = await r.json();
                                if (d.response) return { reply: d.response, sources };
                            }
                        } catch {}
                    }
                    return { reply: fallback(userMessage || ''), sources };
                }

                function fallback(msg) {
                    const m = msg.toLowerCase();
                    if (m.includes('hello') || m.includes('hi'))
                        return ollamaActive ? 'Hello! 👋 How can I help?' : 'Hello! 👋 Limited mode — start Ollama for full AI.';
                    return 'Limited mode. Start Ollama for full AI responses.';
                }

                /* ── Message rendering ────────────────────────── */
                function addRawMessage(html, type) {
                    const c = document.getElementById('chatMessages');
                    const d = document.createElement('div'); d.className = 'message ' + type;
                    const cd = document.createElement('div'); cd.className = 'message-content';
                    cd.innerHTML = html; d.appendChild(cd); c.appendChild(d);
                    c.scrollTop = c.scrollHeight;
                }

                function addBotMessage(text, sources) {
                    const c = document.getElementById('chatMessages');
                    const d = document.createElement('div'); d.className = 'message bot';
                    const cd = document.createElement('div'); cd.className = 'message-content';

                    let f = text;
                    // code blocks first (preserve them)
                    const codeBlocks = [];
                    f = f.replace(/```(\w+)?\n?([\s\S]*?)```/g, function(_, lang, code) {
                        const idx = codeBlocks.length;
                        codeBlocks.push('<pre><code class="language-' + (lang||'text') + '">'
                            + code.replace(/&/g,'&amp;').replace(/</g,'&lt;') + '</code></pre>');
                        return '%%CODE_' + idx + '%%';
                    });
                    f = f.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
                    f = f.replace(/`([^`]+)`/g, '<code>$1</code>');
                    f = f.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
                    f = f.replace(/\n/g, '<br>');
                    codeBlocks.forEach((block, i) => { f = f.replace('%%CODE_' + i + '%%', block); });
                    cd.innerHTML = f;
                    d.appendChild(cd);

                    if (sources && sources.length > 0) {
                        const sd = document.createElement('div');
                        sd.style.cssText = 'margin-top:8px;padding:8px 10px;background:rgba(116,192,252,0.08);border-radius:6px;border-left:3px solid #74c0fc;font-size:12px;';
                        sd.innerHTML =
                        '<div style="color:#74c0fc;font-weight:bold;margin-bottom:4px;">🔗 Sources</div>' +
                        sources.map(function(s) {
                            return '• <a href="' + s.url +
                                '" target="_blank" style="color:#74c0fc;text-decoration:none;">' +
                                s.title.slice(0,60).replace(/</g,'&lt;') +
                                '</a>';
                        }).join('<br>');

                        d.appendChild(sd);
                    }
                    c.appendChild(d); c.scrollTop = c.scrollHeight;
                }

                function escapeHtml(t) {
                    const d = document.createElement('div'); d.textContent = t; return d.innerHTML;
                }

                function showTypingIndicator() {
                    const c = document.getElementById('chatMessages');
                    const d = document.createElement('div'); d.className = 'message bot'; d.id = 'typingIndicator';
                    d.innerHTML = '<div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>';
                    c.appendChild(d); c.scrollTop = c.scrollHeight;
                }

                function hideTypingIndicator() {
                    const el = document.getElementById('typingIndicator'); if (el) el.remove();
                }
            </script>
        </body>
        </html>
        """


class PrivacySettingsDialog(QDialog):
    """Dialog for privacy settings"""
    
    def __init__(self, parent, settings):
        super().__init__(parent)
        self.parent_browser = parent
        self.settings = settings
        self.setWindowTitle("Privacy & Security Settings")
        self.setGeometry(200, 200, 700, 600)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowMaximizeButtonHint)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Proxy Settings
        proxy_group = QGroupBox("🔒 Proxy Settings (VPN)")
        proxy_layout = QVBoxLayout()
        
        self.proxy_enabled = QCheckBox("Enable Proxy/VPN")
        self.proxy_enabled.setChecked(self.settings.get('proxy_enabled', False))
        proxy_layout.addWidget(self.proxy_enabled)
        
        proxy_form = QHBoxLayout()
        proxy_form.addWidget(QLabel("Host:"))
        self.proxy_host = QLineEdit(self.settings.get('proxy_host', ''))
        proxy_form.addWidget(self.proxy_host)
        proxy_form.addWidget(QLabel("Port:"))
        self.proxy_port = QSpinBox()
        self.proxy_port.setRange(0, 65535)
        self.proxy_port.setValue(self.settings.get('proxy_port', 8080))
        proxy_form.addWidget(self.proxy_port)
        proxy_layout.addLayout(proxy_form)
        
        proxy_info = QLabel("ℹ️ Configure your VPN/SOCKS proxy here\nExample: 127.0.0.1:1080 for local SOCKS")
        proxy_info.setWordWrap(True)
        proxy_layout.addWidget(proxy_info)
        
        proxy_group.setLayout(proxy_layout)
        layout.addWidget(proxy_group)
        
        # DNS Settings
        dns_group = QGroupBox("🌐 Secure DNS Settings")
        dns_layout = QVBoxLayout()
        
        dns_info = QLabel("Select your preferred secure DNS provider:")
        dns_layout.addWidget(dns_info)
        
        self.dns_combo = QComboBox()
        for name, config in DNS_SERVERS.items():
            self.dns_combo.addItem(f"{name} - {config['description']}", name)
        
        current_dns = self.settings.get('dns_provider', 'Cloudflare')
        index = self.dns_combo.findData(current_dns)
        if index >= 0:
            self.dns_combo.setCurrentIndex(index)
        
        dns_layout.addWidget(self.dns_combo)
        
        dns_details = QLabel(f"Primary: {DNS_SERVERS[current_dns]['primary']}\nSecondary: {DNS_SERVERS[current_dns]['secondary']}")
        dns_layout.addWidget(dns_details)
        
        self.dns_combo.currentIndexChanged.connect(lambda: self.update_dns_details(dns_details))
        
        dns_group.setLayout(dns_layout)
        layout.addWidget(dns_group)
        
        # Search Engine Settings (Backend for My Browser)
        engine_group = QGroupBox("🔍 My Browser Search Engine (Backend)")
        engine_layout = QVBoxLayout()
        
        engine_info = QLabel("Select which search engine 'My Browser' uses internally:")
        engine_layout.addWidget(engine_info)
        
        self.backend_engine_combo = QComboBox()
        for name, config in SEARCH_ENGINES.items():
            self.backend_engine_combo.addItem(f"{config['icon']} {name} - {config['description']}", name)
        
        current_backend = self.settings.get('backend_search_engine', 'Brave Search')
        index = self.backend_engine_combo.findData(current_backend)
        if index >= 0:
            self.backend_engine_combo.setCurrentIndex(index)
        
        engine_layout.addWidget(self.backend_engine_combo)
        
        engine_note = QLabel("ℹ️ This determines which search engine powers 'My Browser'.\nYou'll still see your custom homepage, not the search engine's page.")
        engine_note.setWordWrap(True)
        engine_layout.addWidget(engine_note)
        
        engine_group.setLayout(engine_layout)
        layout.addWidget(engine_group)
        
        # Privacy Logging
        logging_group = QGroupBox("📝 Privacy Logging")
        logging_layout = QVBoxLayout()
        
        self.logging_enabled = QCheckBox("Enable Search & Browse Logging (for your privacy audit)")
        self.logging_enabled.setChecked(self.settings.get('logging_enabled', True))
        logging_layout.addWidget(self.logging_enabled)
        
        log_info = QLabel("All searches and page visits are logged locally for your review.\nLogs are encrypted and stored only on your device.")
        log_info.setWordWrap(True)
        logging_layout.addWidget(log_info)
        
        view_logs_btn = QPushButton("📊 View Search Logs")
        view_logs_btn.clicked.connect(self.view_logs)
        logging_layout.addWidget(view_logs_btn)
        
        logging_group.setLayout(logging_layout)
        layout.addWidget(logging_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Save Settings")
        save_btn.clicked.connect(self.save_settings)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def update_dns_details(self, label):
        dns_name = self.dns_combo.currentData()
        dns = DNS_SERVERS[dns_name]
        label.setText(f"Primary: {dns['primary']}\nSecondary: {dns['secondary']}")
    
    def save_settings(self):
        self.settings['proxy_enabled'] = self.proxy_enabled.isChecked()
        self.settings['proxy_host'] = self.proxy_host.text()
        self.settings['proxy_port'] = self.proxy_port.value()
        self.settings['dns_provider'] = self.dns_combo.currentData()
        self.settings['backend_search_engine'] = self.backend_engine_combo.currentData()
        self.settings['logging_enabled'] = self.logging_enabled.isChecked()
        
        self.parent_browser.save_settings()
        self.parent_browser.apply_privacy_settings()
        
        QMessageBox.information(self, "Success", "Settings saved!\n\nYour 'My Browser' will now use " + self.backend_engine_combo.currentData() + " for searches.")
        self.close()
    
    def view_logs(self):
        log_viewer = SearchLogViewer(self, self.parent_browser.privacy_logger)
        log_viewer.show()


class SearchLogViewer(QDialog):
    """View search and privacy logs — resizable, shows searches + page visits"""

    def __init__(self, parent, logger):
        super().__init__(parent)
        self.logger = logger
        self.setWindowTitle("Search & Privacy Logs")
        self.setGeometry(150, 80, 1100, 750)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowMaximizeButtonHint)
        self.setup_ui()

    def setup_ui(self):
        from PyQt6.QtWidgets import QTabWidget, QWidget
        layout = QVBoxLayout()

        tabs = QTabWidget()

        # ── Tab 1: Searches ────────────────────────────────────────────────
        t1 = QWidget(); t1l = QVBoxLayout()
        t1l.addWidget(QLabel("🔍  Every search you performed — stored locally on your device"))

        self.search_text = QTextEdit()
        search_text = self.search_text
        search_text.setReadOnly(True)
        search_text.setFont(QFont("Courier New", 10))

        lines = []
        try:
            if os.path.exists(self.logger.privacy_log_file):
                with open(self.logger.privacy_log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                searches = [l for l in logs if l.get('type') == 'search']
                for s in reversed(searches[-500:]):
                    lines.append(f"[{s['timestamp']}]  {s.get('engine','?'):<20}  {s.get('query','')}")
        except Exception:
            pass
        if not lines:
            try:
                if os.path.exists(self.logger.search_log_file):
                    with open(self.logger.search_log_file, 'r', encoding='utf-8') as f:
                        raw = f.readlines()
                    lines = [l.rstrip() for l in reversed(raw[-500:])]
            except Exception:
                pass

        if lines:
            search_text.setText("\n".join(lines))
        else:
            search_text.setText(
                "No searches logged yet.\n\n"
                "Searches are recorded when you type in the URL bar or home page search.\n"
                f"Log file: {self.logger.search_log_file}"
            )
        t1l.addWidget(search_text)
        t1.setLayout(t1l)
        tabs.addTab(t1, f"🔍 Searches ({len(lines)})")

        # ── Tab 2: Page Visits ─────────────────────────────────────────────
        t2 = QWidget(); t2l = QVBoxLayout()
        t2l.addWidget(QLabel("🌐  Every page you visited — recorded locally"))

        self.visit_text = QTextEdit()
        visit_text = self.visit_text
        visit_text.setReadOnly(True)
        visit_text.setFont(QFont("Courier New", 10))

        visit_lines = []
        try:
            if os.path.exists(self.logger.privacy_log_file):
                with open(self.logger.privacy_log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                visits = [l for l in logs if l.get('type') == 'visit']
                for v in reversed(visits[-500:]):
                    title = v.get('title', '')[:35]
                    url   = v.get('url', '')
                    visit_lines.append(f"[{v['timestamp']}]  {title:<35}  {url}")
        except Exception:
            pass

        if visit_lines:
            visit_text.setText("\n".join(visit_lines))
        else:
            visit_text.setText(
                "No page visits logged yet.\n\n"
                "Page visits are recorded when a page finishes loading.\n"
                f"Log file: {self.logger.privacy_log_file}"
            )
        t2l.addWidget(visit_text)
        t2.setLayout(t2l)
        tabs.addTab(t2, f"🌐 Page Visits ({len(visit_lines)})")

        layout.addWidget(tabs)

        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(lambda: [self.close(), SearchLogViewer(self.parent(), self.logger).show()])
        btn_layout.addWidget(refresh_btn)
        export_btn = QPushButton("💾 Export")
        export_btn.clicked.connect(self.export_logs)
        btn_layout.addWidget(export_btn)
        clear_btn = QPushButton("🗑️ Clear Logs")
        clear_btn.clicked.connect(self.clear_logs)
        btn_layout.addWidget(clear_btn)
        close_btn = QPushButton("✖ Close")
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def export_logs(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export Logs", "", "Text Files (*.txt)")
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.search_text.toPlainText())
                f.write("\n\n--- PAGE VISITS ---\n\n")
                f.write(self.visit_text.toPlainText())
            QMessageBox.information(self, "Success", "Logs exported successfully!")
    
    def clear_logs(self):
        reply = QMessageBox.question(self, "Clear Logs", 
                                     "Are you sure you want to clear all logs?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if os.path.exists(self.logger.search_log_file):
                    os.remove(self.logger.search_log_file)
                if os.path.exists(self.logger.privacy_log_file):
                    os.remove(self.logger.privacy_log_file)
                self.search_text.clear()
                self.visit_text.clear()
                QMessageBox.information(self, "Success", "Logs cleared!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to clear logs: {e}")


class ExtensionsDialog(QDialog):
    """Manage browser extensions"""
    
    def __init__(self, parent, extension_manager):
        super().__init__(parent)
        self.parent_browser = parent
        self.ext_manager = extension_manager
        self.setWindowTitle("🧩 Browser Extensions")
        self.setGeometry(200, 200, 700, 500)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowMaximizeButtonHint)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        info = QLabel("🧩 Manage your browser extensions")
        layout.addWidget(info)
        
        self.ext_list = QListWidget()
        self.refresh_list()
        layout.addWidget(self.ext_list)
        
        btn_layout = QHBoxLayout()
        toggle_btn = QPushButton("🔄 Toggle On/Off")
        toggle_btn.clicked.connect(self.toggle_extension)
        add_btn = QPushButton("➕ Add Extension")
        add_btn.clicked.connect(self.add_extension)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        
        btn_layout.addWidget(toggle_btn)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def refresh_list(self):
        self.ext_list.clear()
        for ext in self.ext_manager.extensions:
            status = "✅" if ext['enabled'] else "❌"
            builtin = "🔧" if ext['builtin'] else "👤"
            self.ext_list.addItem(f"{status} {builtin} {ext['name']}")
    
    def toggle_extension(self):
        current_row = self.ext_list.currentRow()
        if current_row >= 0:
            ext = self.ext_manager.extensions[current_row]
            new_state = self.ext_manager.toggle_extension(ext['name'])
            self.refresh_list()
            
            # Reload all tabs to apply/remove the extension
            for i in range(self.parent_browser.tabs.count()):
                tab_widget = self.parent_browser.tabs.widget(i)
                if tab_widget and hasattr(tab_widget, 'browser'):
                    # Save current URL
                    current_url = tab_widget.browser.url()
                    # Reload the page to reapply scripts
                    tab_widget.browser.reload()
            
            status = "enabled" if new_state else "disabled"
            QMessageBox.information(self, "Success", f"Extension '{ext['name']}' {status}!\nAll tabs have been reloaded.")
    
    def add_extension(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Extension (.js file)", "", "JavaScript (*.js)")
        if filename:
            import shutil
            dest = os.path.join(self.ext_manager.extension_dir, os.path.basename(filename))
            shutil.copy(filename, dest)
            self.ext_manager.extensions = self.ext_manager.load_extensions()
            self.refresh_list()
            QMessageBox.information(self, "Success", "Extension added!")


class CustomBrowserTab(QWidget):
    """Browser tab with privacy features and extensions"""
    
    def __init__(self, profile, engine_name, parent, extension_manager):
        super().__init__(parent)
        self.engine_name = engine_name
        self.engine_config = BROWSERS[engine_name]
        self.parent_browser = parent
        self.ext_manager = extension_manager
        
        self.page = QWebEnginePage(profile, self)
        self.browser = QWebEngineView()
        self.browser.setPage(self.page)
        
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.browser)
        self.setLayout(layout)
        
        # ONLY apply custom branding if this is "My Browser" engine
        if engine_name == 'My Browser':
            self.apply_custom_browser_theme()
        
        # Apply extensions to all tabs
        self.apply_extensions()
    
    def apply_custom_browser_theme(self):
        """Apply My Browser branding"""
        custom_css = """
        #header, .brave-logo, [class*="brave"], [id*="brave"],
        header, nav.top-nav, .search-header, .header-wrapper,
        .logo-container, .brand-logo, img[alt*="Brave"], img[src*="brave"],
        a[href*="brave.com"] img { display: none !important; }
        
        body:before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 70px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            z-index: 9999;
        }
        
        body:after {
            content: '🦕 My Browser';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 70px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            font-weight: 700;
            color: white;
            z-index: 10000;
            pointer-events: none;
        }
        
        body { padding-top: 70px !important; }
        """
        
        script = QWebEngineScript()
        script.setName("my-browser-theme")
        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentReady)
        script.setSourceCode(f"(function(){{var s=document.createElement('style');s.textContent=`{custom_css}`;document.head.appendChild(s);}})();")
        self.page.scripts().insert(script)
    
    def apply_extensions(self):
        """Apply all enabled extensions"""
        for i, code in enumerate(self.ext_manager.get_enabled_scripts()):
            script = QWebEngineScript()
            script.setName(f"extension-{i}")
            script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentReady)
            script.setSourceCode(code)
            self.page.scripts().insert(script)
    
    def load_url(self, url):
        self.browser.setUrl(QUrl(url))


class ModernBrowser(QMainWindow):
    """Advanced privacy-focused browser"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Browser - Privacy Edition")
        self.setGeometry(100, 100, 1400, 900)
        # Explicitly request all three window control buttons (close / minimize / maximize)
        # Without this some Linux window managers omit the minimize button with Qt6.
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowCloseButtonHint |
            Qt.WindowType.WindowMinimizeButtonHint |
            Qt.WindowType.WindowMaximizeButtonHint
        )
        
        # Setup directories
        self.data_dir = os.path.expanduser("~/.mybrowser")
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.history_file = os.path.join(self.data_dir, "history.json")
        self.bookmarks_file = os.path.join(self.data_dir, "bookmarks.json")
        self.settings_file = os.path.join(self.data_dir, "settings.json")
        
        # Initialize components
        self.history = self.load_history()
        self.bookmarks = self.load_bookmarks()
        self.settings = self.load_settings()
        self.current_search_engine = self.settings.get('browser', DEFAULT_BROWSER)
        
        # Privacy components
        self.privacy_logger = PrivacyLogger(self.data_dir)

        # Optional microservices
        self.network_interceptor = NetworkRequestInterceptor() if MODULES_AVAILABLE else None
        self.security_monitor = SecurityMonitor() if MODULES_AVAILABLE else None

        self.extension_manager = ExtensionManager(os.path.join(self.data_dir, "extensions"))

        # ── MICROSERVICES INIT ────────────────────────────────────
        if MODULES_AVAILABLE:
            self.network_interceptor = NetworkRequestInterceptor()
            self.ip_masking          = IPMaskingMonitor()
            self.social_tabs         = SocialTabManager(self)
            self.security_monitor    = SecurityMonitor()
            self.network_interceptor.request_logged.connect(self._on_request_logged)
            self.ip_masking.ip_changed.connect(self._on_ip_changed)
            self.security_monitor.alert_triggered.connect(self._on_security_alert)
        else:
            self.network_interceptor = None
            self.ip_masking          = None
            self.social_tabs         = None
            self.security_monitor    = None
        # ──────────────────────────────────────────────────────────
        
        # Create profile
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.downloadRequested.connect(self.handle_download)
        
        # UI Setup (create status bar first!)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.setCentralWidget(self.tabs)
        
        self.create_modern_navigation_bar()
        self.create_menu_bar()
        self.apply_dynamic_theme()
        self.update_status_bar_theme()
        
        # Apply privacy settings (after status bar is created)
        self.apply_privacy_settings()
        
        # ALWAYS open with My Browser homepage (don't restore last session)
        # This ensures consistent startup experience
        self.current_search_engine = DEFAULT_SEARCH_ENGINE
        self.settings['search_engine'] = DEFAULT_SEARCH_ENGINE
        self.save_settings()
        
        # Open initial tab with My Browser
        self.add_new_tab_with_engine(DEFAULT_SEARCH_ENGINE)
        
        # Make sure the engine selector shows My Browser
        index = self.engine_selector.findData(DEFAULT_SEARCH_ENGINE)
        if index >= 0:
            self.engine_selector.setCurrentIndex(index)
        
        self.downloads = []
        
        # Start chatbot attach-button polling from the beginning so the
        # 🖼️ / 📎 buttons inside the chatbot window work immediately on first click.
        self._setup_attach_polling()
        
        # Show privacy indicator
        self.update_privacy_indicator()
    
    def apply_privacy_settings(self):
        """Apply privacy and security settings"""
        # Apply proxy if enabled
        if self.settings.get('proxy_enabled', False):
            proxy_host = self.settings.get('proxy_host', '')
            proxy_port = self.settings.get('proxy_port', 8080)
            
            if proxy_host:
                proxy = QNetProxy()
                proxy.setType(QNetProxy.ProxyType.HttpProxy)
                proxy.setHostName(proxy_host)
                proxy.setPort(proxy_port)
                QNetProxy.setApplicationProxy(proxy)
                self.status.showMessage(f"🔒 Proxy enabled: {proxy_host}:{proxy_port}", 5000)
        else:
            QNetProxy.setApplicationProxy(QNetProxy())
        
        # DNS settings (informational - actual DNS change requires system-level changes)
        dns_provider = self.settings.get('dns_provider', 'Cloudflare')
        dns = DNS_SERVERS[dns_provider]
        self.status.showMessage(f"🌐 DNS: {dns_provider} ({dns['primary']})", 3000)
    
    def update_privacy_indicator(self):
        """Update privacy status in title bar"""
        indicators = []
        if self.settings.get('proxy_enabled', False):
            indicators.append("🔒 VPN")
        if self.settings.get('logging_enabled', True):
            indicators.append("📝 Logged")
        
        dns = self.settings.get('dns_provider', 'Cloudflare')
        indicators.append(f"🌐 {dns}")
        
        status = " | ".join(indicators)
        self.setWindowTitle(f"My Browser - {status}")
    
    def log_search(self, query):
        """Log a search query"""
        if self.settings.get('logging_enabled', True):
            self.privacy_logger.log_search(query, self.current_search_engine)
    
    def navigate_to_url(self):
        """Navigate with search logging"""
        q = self.url_bar.text().strip()
        if not q:
            return
        browser = self.current_browser()
        if browser:
            if q.startswith('http://') or q.startswith('https://'):
                url = q
            elif '.' in q and ' ' not in q:
                url = 'http://' + q
            else:
                # Plain keyword — log immediately
                self.log_search(q)
                if self.current_search_engine == 'My Browser':
                    backend_engine = self.settings.get('backend_search_engine', 'Brave Search')
                    search_url = SEARCH_ENGINES[backend_engine]['search_url']
                else:
                    search_url = BROWSERS[self.current_search_engine]['search_url']
                url = search_url.format(q.replace(' ', '+'))
            browser.setUrl(QUrl(url))
    
    def create_modern_navigation_bar(self):
        navbar = QToolBar("Navigation")
        navbar.setIconSize(QSize(24, 24))
        navbar.setMovable(False)
        self.addToolBar(navbar)
        
        navbar.setStyleSheet("""
            QToolBar { background: rgba(255, 255, 255, 0.1); border: none; padding: 8px; }
            QToolButton { background: rgba(255, 255, 255, 0.15); border: none; border-radius: 8px; 
                         padding: 8px; color: white; font-weight: 600; }
            QToolButton:hover { background: rgba(255, 255, 255, 0.25); }
        """)
        
        back_btn = QAction("←", self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        navbar.addAction(back_btn)
        
        forward_btn = QAction("→", self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        navbar.addAction(forward_btn)
        
        reload_btn = QAction("↻", self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        navbar.addAction(reload_btn)
        
        home_btn = QAction("⌂", self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)
        
        self.engine_selector = QComboBox()
        for browser_name, config in BROWSERS.items():
            self.engine_selector.addItem(f"{config['icon']} {browser_name}", browser_name)
        index = self.engine_selector.findData(self.current_search_engine)
        if index >= 0:
            self.engine_selector.setCurrentIndex(index)
        self.engine_selector.currentIndexChanged.connect(self.change_search_engine)
        
        self.engine_selector.setStyleSheet("""
            QComboBox { background: rgba(255, 255, 255, 0.2); border: 2px solid rgba(255, 255, 255, 0.3);
                       border-radius: 10px; padding: 8px 12px; color: white; font-size: 14px; min-width: 180px; }
        """)
        navbar.addWidget(self.engine_selector)
        
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setPlaceholderText("🔍 Search privately or enter URL...")
        self.url_bar.setStyleSheet("""
            QLineEdit { background: rgba(255, 255, 255, 0.9); border: 2px solid rgba(255, 255, 255, 0.3);
                       border-radius: 12px; padding: 10px 15px; font-size: 14px; color: #1a1a2e; }
        """)
        navbar.addWidget(self.url_bar)
        
        new_tab_btn = QAction("+", self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab_with_engine(self.current_search_engine))
        navbar.addAction(new_tab_btn)

        # ── SOCIAL DROPDOWN ──────────────────────────────────────
        if MODULES_AVAILABLE and self.social_tabs:
            from PyQt6.QtWidgets import QToolButton, QMenu
            social_btn = QToolButton()
            social_btn.setText("🌍 Social")
            social_btn.setToolTip("Open Social Media")
            social_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
            social_btn.setStyleSheet("""
                QToolButton {
                    background: rgba(255,255,255,0.15); color: white;
                    border: 1px solid rgba(255,255,255,0.3);
                    border-radius: 8px; padding: 6px 12px; font-size: 13px;
                }
                QToolButton:hover { background: rgba(255,255,255,0.28); }
                QToolButton::menu-indicator { image: none; }
            """)
            social_menu = QMenu(social_btn)
            social_menu.setStyleSheet("""
                QMenu {
                    background: rgba(20,20,50,0.97); color: white;
                    border-radius: 10px; padding: 6px;
                }
                QMenu::item { padding: 10px 24px; border-radius: 6px; font-size: 13px; }
                QMenu::item:selected { background: rgba(255,255,255,0.2); }
            """)
            for pid, pdata in self.social_tabs.get_all_platforms().items():
                _pid = pid; _pdata = pdata
                if pdata.get('name','').lower() == 'whatsapp' or pid.lower() == 'whatsapp':
                    _pid = 'facebook'; _pdata = {'name': 'Facebook', 'url': 'https://www.facebook.com', 'icon': '📘'}
                act = QAction(f"{_pdata['icon']}  {_pdata['name']}", self)
                act.triggered.connect(lambda chk, p=_pid: self._open_social(p))
                social_menu.addAction(act)
            social_btn.setMenu(social_menu)
            navbar.addSeparator()
            navbar.addWidget(social_btn)
        # ─────────────────────────────────────────────────────────
        # NOTE: 🖼️ / 📎 attach buttons live inside the chatbot window only.
        # Python polls window._attachImageRequested / _attachFileRequested flags
        # (set by those in-chatbot buttons) and opens QFileDialog from there.
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar { background: rgba(0, 0, 0, 0.2); color: white; padding: 5px; }
            QMenu { background: rgba(30, 30, 60, 0.95); color: white; border-radius: 8px; }
        """)
        
        # File menu
        file_menu = menubar.addMenu("&File")
        file_menu.addAction(QAction("New Tab", self, triggered=lambda: self.add_new_tab_with_engine(self.current_search_engine)))
        
        # Privacy menu
        privacy_menu = menubar.addMenu("🔒 &Privacy")
        privacy_menu.addAction(QAction("Privacy Settings", self, triggered=self.show_privacy_settings))
        privacy_menu.addAction(QAction("View Search Logs", self, triggered=self.show_search_logs))
        privacy_menu.addSeparator()
        privacy_menu.addAction(QAction("Clear Browsing Data", self, triggered=self.clear_browsing_data))
        
        # Extensions menu
        ext_menu = menubar.addMenu("🧩 &Extensions")
        ext_menu.addAction(QAction("Manage Extensions", self, triggered=self.show_extensions))
        
        # Bookmarks
        bookmarks_menu = menubar.addMenu("&Bookmarks")
        bookmarks_menu.addAction(QAction("Add Bookmark", self, shortcut="Ctrl+D", triggered=self.add_bookmark))
        bookmarks_menu.addAction(QAction("Show Bookmarks", self, triggered=self.show_bookmarks))

        # ── SECURITY MENU ─────────────────────────────────────────
        if MODULES_AVAILABLE and self.network_interceptor:
            sec_menu = menubar.addMenu("🛡️ &Security")

            act = QAction("🌐 Network Monitor", self)
            act.setStatusTip("See every request your browser makes and blocked ads/trackers")
            act.triggered.connect(self._show_network_monitor)
            sec_menu.addAction(act)

            act2 = QAction("🎭 IP Masking", self)
            act2.setStatusTip("View & apply IP address masking algorithms")
            act2.triggered.connect(self._show_ip_masking)
            sec_menu.addAction(act2)

            act3 = QAction("🛡️ Security Dashboard", self)
            act3.setStatusTip("Security health score and threat alerts")
            act3.triggered.connect(self._show_security_dashboard)
            sec_menu.addAction(act3)

            sec_menu.addSeparator()

            act4 = QAction("📡 P2P Send File", self)
            act4.setStatusTip("Send a file directly to another computer on your network")
            act4.triggered.connect(self._show_p2p_send)
            sec_menu.addAction(act4)

            act5 = QAction("📥 P2P Receive File", self)
            act5.setStatusTip("Receive a file sent from another computer")
            act5.triggered.connect(self._show_p2p_receive)
            sec_menu.addAction(act5)
        # ──────────────────────────────────────────────────────────
    
    def show_privacy_settings(self):
        dialog = PrivacySettingsDialog(self, self.settings)
        dialog.show()
        self.update_privacy_indicator()
    
    def show_search_logs(self):
        viewer = SearchLogViewer(self, self.privacy_logger)
        viewer.show()
    
    def show_extensions(self):
        dialog = ExtensionsDialog(self, self.extension_manager)
        dialog.show()
    
    def clear_browsing_data(self):
        reply = QMessageBox.question(self, "Clear Data",
                                     "Clear all browsing data (history, cache, cookies)?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.history = []
            self.save_history()
            self.profile.clearAllVisitedLinks()
            QMessageBox.information(self, "Success", "Browsing data cleared!")
    
    def apply_dynamic_theme(self):
        engine = BROWSERS[self.current_search_engine]
        self.setStyleSheet(f"""
            QMainWindow {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                          stop:0 {engine['gradient_start']}, stop:1 {engine['gradient_end']}); }}
            QTabBar::tab {{ background: rgba(255, 255, 255, 0.1); color: white; padding: 12px 24px;
                           border-top-left-radius: 8px; border-top-right-radius: 8px; }}
            QTabBar::tab:selected {{ background: rgba(255, 255, 255, 0.25); }}
        """)
    
    def update_status_bar_theme(self):
        self.status.setStyleSheet("QStatusBar { background: rgba(0, 0, 0, 0.3); color: white; }")
    
    def change_search_engine(self, index):
        engine_name = self.engine_selector.itemData(index)
        if engine_name:
            self.current_search_engine = engine_name
            self.settings['browser'] = engine_name
            self.save_settings()
            self.apply_dynamic_theme()
            
            # Get current tab widget
            current_tab = self.tabs.currentWidget()
            
            # Remove current tab
            if current_tab:
                current_index = self.tabs.currentIndex()
                self.tabs.removeTab(current_index)
            
            # Create new tab with selected engine
            self.add_new_tab_with_engine(engine_name)
            
            # Update privacy indicator
            self.update_privacy_indicator()
    
    def add_new_tab_with_engine(self, engine_name):
        tab = CustomBrowserTab(self.profile, engine_name, self, self.extension_manager)
        i = self.tabs.addTab(tab, f"{BROWSERS[engine_name]['icon']} New Tab")
        self.tabs.setCurrentIndex(i)
        
        engine_url = BROWSERS[engine_name]['url']
        if engine_url == 'about:home':
            tab.browser.setHtml(CustomSearchPage.get_html())
        else:
            tab.load_url(engine_url)
        
        # Fixed: Use a proper connection that doesn't reference tab after deletion
        def on_url_changed(qurl):
            browser = tab.browser
            if browser and browser == self.current_browser():
                url_string = qurl.toString()
                if not url_string.startswith('about:'):
                    self.url_bar.setText(url_string)
                    self.url_bar.setCursorPosition(0)
            # ── Log to network interceptor (makes Network Monitor work) ──
            url_str = qurl.toString()
            if url_str and not url_str.startswith('about:') and self.network_interceptor:
                self.network_interceptor.log_request(url_str, 'GET')
        
        def on_load_finished(success):
            if not success:
                return
                
            title = tab.browser.page().title() if tab.browser else "New Tab"
            url = tab.browser.url().toString() if tab.browser else ""

            # Extract and log search query from search engine URLs
            if url and not url.startswith('about:'):
                try:
                    from urllib.parse import urlparse, parse_qs
                    parsed = urlparse(url)
                    qs = parse_qs(parsed.query)
                    # q= param used by Google, Brave, DDG, Bing, Ecosia, Startpage, Qwant, Searx, GitHub
                    # p= used by Yahoo, text= by Yandex, search= by Wikipedia
                    query = None
                    for param in ('q', 'p', 'text', 'search', 'query', 'search_query'):
                        if param in qs and qs[param][0].strip():
                            query = qs[param][0].strip()
                            break
                    if query:
                        self.log_search(query)
                except Exception:
                    pass

            # Log to privacy logger
            if url and not url.startswith('about:'):
                self.privacy_logger.log_page_visit(url, title)
            
            # Add to browsing history
            if url and not url.startswith('about:'):
                # Check if this URL is already the last entry (avoid duplicates)
                if not self.history or self.history[-1].get('url') != url:
                    self.history.append({
                        'url': url,
                        'title': title or "Untitled",
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    # Keep only last 1000 entries
                    if len(self.history) > 1000:
                        self.history = self.history[-1000:]
                    self.save_history()
            
            # Update tab title
            if not title:
                title = "New Tab"
            if len(title) > 20:
                title = title[:20] + "..."
            self.tabs.setTabText(i, f"{BROWSERS[self.current_search_engine]['icon']} {title}")
        
        tab.browser.urlChanged.connect(on_url_changed)
        tab.browser.loadFinished.connect(on_load_finished)
    
    def navigate_home(self):
        browser = self.current_browser()
        if browser:
            if BROWSERS[self.current_search_engine]['url'] == 'about:home':
                browser.setHtml(CustomSearchPage.get_html())
            else:
                browser.setUrl(QUrl(BROWSERS[self.current_search_engine]['url']))
    
    def current_browser(self):
        try:
            widget = self.tabs.currentWidget()
            return widget.browser if widget and hasattr(widget, 'browser') else None
        except RuntimeError:
            return None
    
    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)
    
    def current_tab_changed(self, i):
        browser = self.current_browser()
        if browser:
            url_string = browser.url().toString()
            if not url_string.startswith('about:'):
                self.url_bar.setText(url_string)
                self.url_bar.setCursorPosition(0)
    
    def load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def save_history(self):
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except:
            pass
    
    def load_bookmarks(self):
        try:
            if os.path.exists(self.bookmarks_file):
                with open(self.bookmarks_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def save_bookmarks(self):
        try:
            with open(self.bookmarks_file, 'w') as f:
                json.dump(self.bookmarks, f, indent=2)
        except:
            pass
    
    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except:
            pass
    
    def add_bookmark(self):
        browser = self.current_browser()
        if browser:
            url = browser.url().toString()
            title = browser.page().title() or "Untitled"
            name, ok = QInputDialog.getText(self, 'Add Bookmark', 'Name:', text=title)
            if ok and name:
                self.bookmarks.append({'title': name, 'url': url, 'added': datetime.now().isoformat()})
                self.save_bookmarks()
                QMessageBox.information(self, 'Success', 'Bookmark added!')
    
    def show_bookmarks(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Bookmarks")
        dialog.setGeometry(200, 200, 600, 400)
        dialog.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowMaximizeButtonHint)
        layout = QVBoxLayout()
        
        list_widget = QListWidget()
        for bm in self.bookmarks:
            list_widget.addItem(f"{bm['title']} - {bm['url']}")
        layout.addWidget(list_widget)
        
        btn_layout = QHBoxLayout()
        open_btn = QPushButton("Open")
        open_btn.clicked.connect(lambda: self.open_bookmark(list_widget, dialog))
        btn_layout.addWidget(open_btn)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        dialog.setLayout(layout)
        dialog.show()
    
    def open_bookmark(self, list_widget, dialog):
        row = list_widget.currentRow()
        if 0 <= row < len(self.bookmarks):
            self.current_browser().setUrl(QUrl(self.bookmarks[row]['url']))
            dialog.close()
    
    def handle_download(self, download):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", download.downloadFileName())
        if path:
            download.setDownloadDirectory(os.path.dirname(path))
            download.setDownloadFileName(os.path.basename(path))
            download.accept()




    # ════════════════════════════════════════════════════════════
    #  MICROSERVICES METHODS
    # ════════════════════════════════════════════════════════════

    # ── Signal handlers ──────────────────────────────────────────
    def _on_request_logged(self, url, method, blocked):
        if blocked and self.security_monitor:
            self.security_monitor.log_alert('MEDIUM', f'Blocked: {url[:60]}', 'network')

    def _on_ip_changed(self, original, masked, algorithm):
        self.statusBar().showMessage(f"🎭 IP: {original} → {masked} [{algorithm}]", 5000)

    def _on_security_alert(self, level, message):
        icons = {'LOW':'🟢','MEDIUM':'🟡','HIGH':'🔴','CRITICAL':'🚨'}
        self.statusBar().showMessage(f"{icons.get(level,'⚠️')} {message}", 3000)

    # ── Social tab opener ─────────────────────────────────────────
    def _open_social(self, platform_id):
        """Open social platform in new tab using existing CustomBrowserTab"""
        if not self.social_tabs:
            return
        _all = self.social_tabs.get_all_platforms()
        if platform_id == 'facebook':
            platform = {'name': 'Facebook', 'url': 'https://www.facebook.com', 'icon': '📘'}
        else:
            platform = _all.get(platform_id)
            if platform and platform.get('name','').lower() == 'whatsapp':
                platform = {'name': 'Facebook', 'url': 'https://www.facebook.com', 'icon': '📘'}
        if not platform:
            return

        from PyQt6.QtCore import QUrl

        # Create a new tab using the first engine (My Browser)
        engine_name = list(BROWSERS.keys())[0]
        tab = CustomBrowserTab(self.profile, engine_name, self, self.extension_manager)
        i = self.tabs.addTab(tab, f"{platform['icon']} {platform['name']}")
        self.tabs.setCurrentIndex(i)
        tab.browser.load(QUrl(platform['url']))

        def on_title(title):
            try:
                idx = self.tabs.indexOf(tab)
                if idx >= 0 and title:
                    self.tabs.setTabText(idx, f"{platform['icon']} {title[:18]}")
            except RuntimeError:
                pass  # Tab or widget was deleted
        tab.browser.titleChanged.connect(on_title)

        def on_url(qurl):
            if tab.browser == self.current_browser():
                u = qurl.toString()
                if not u.startswith('about:'):
                    self.url_bar.setText(u)
                    self.url_bar.setCursorPosition(0)
        tab.browser.urlChanged.connect(on_url)

    # ── Network Monitor ───────────────────────────────────────────
    def _show_network_monitor(self):
        """Network Monitor — live request log + blocked domain manager"""
        if not self.network_interceptor:
            return
        from PyQt6.QtWidgets import (
            QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
            QTableWidgetItem, QHeaderView, QPushButton, QLineEdit,
            QTabWidget, QWidget, QListWidget, QListWidgetItem, QMessageBox
        )
        from PyQt6.QtGui import QColor, QFont
        from PyQt6.QtCore import Qt

        dlg = QMainWindow()
        dlg.setWindowTitle("🌐 Network Monitor")
        dlg.setGeometry(100, 100, 1060, 720)
        dlg.setStyleSheet("background:#0f0f23; color:white;")
        main_lay = QVBoxLayout()

        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane { border:1px solid #333; border-radius:6px; }
            QTabBar::tab { background:#1e1e3a; color:#aaa; padding:8px 18px;
                           border-radius:6px 6px 0 0; margin-right:2px; }
            QTabBar::tab:selected { background:#2a2a5a; color:white; font-weight:bold; }
        """)

        # ── TAB 1: Live Request Log ───────────────────────────────────────────
        tab1 = QWidget(); t1l = QVBoxLayout()

        hdr = QLabel(
            "Every HTTP/HTTPS request your browser makes is listed here.\n"
            "✅ ALLOWED = went through normally   "
            "🚫 BLOCKED = matched a blocked domain and was stopped"
        )
        hdr.setWordWrap(True)
        hdr.setStyleSheet(
            "background:rgba(255,255,255,0.07);padding:10px;"
            "border-radius:8px;font-size:12px;")
        t1l.addWidget(hdr)

        s = self.network_interceptor.get_stats()
        stats_lbl = QLabel(
            f"📊 Total: {s['total']}     ✅ Allowed: {s['allowed']}     🚫 Blocked: {s['blocked']}"
        )
        stats_lbl.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        stats_lbl.setStyleSheet(
            "padding:10px;background:rgba(255,255,255,0.1);border-radius:8px;")
        t1l.addWidget(stats_lbl)

        reqs = self.network_interceptor.get_recent_requests(200)
        tbl = QTableWidget(len(reqs), 4)
        tbl.setHorizontalHeaderLabels(["Time", "Method", "URL", "Status"])
        tbl.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        tbl.setColumnWidth(0, 80); tbl.setColumnWidth(1, 65); tbl.setColumnWidth(3, 120)
        tbl.setStyleSheet(
            "QTableWidget{background:#12122a;color:white;gridline-color:#2a2a4a;}"
            "QHeaderView::section{background:#2a2a4a;color:white;padding:6px;}")
        for i, r in enumerate(reversed(reqs)):
            tbl.setItem(i, 0, QTableWidgetItem(r["timestamp"][11:19]))
            tbl.setItem(i, 1, QTableWidgetItem(r.get("method","GET")))
            tbl.setItem(i, 2, QTableWidgetItem(r["url"][:120]))
            blk = r["blocked"]
            si = QTableWidgetItem("🚫 BLOCKED" if blk else "✅ ALLOWED")
            si.setForeground(QColor("#ff6b6b") if blk else QColor("#51cf66"))
            tbl.setItem(i, 3, si)
        t1l.addWidget(tbl)

        b1 = QHBoxLayout()
        clr = QPushButton("🗑️ Clear Log")
        clr.setStyleSheet("background:#e74c3c;color:white;padding:8px 16px;border-radius:6px;")
        clr.clicked.connect(lambda: [self.network_interceptor.clear_log(), dlg.close()])
        b1.addWidget(clr)
        cls1 = QPushButton("✖ Close")
        cls1.setStyleSheet("background:#555;color:white;padding:8px 16px;border-radius:6px;")
        cls1.clicked.connect(dlg.close)
        b1.addWidget(cls1)
        t1l.addLayout(b1)
        tab1.setLayout(t1l)
        tabs.addTab(tab1, "📋 Live Request Log")

        # ── TAB 2: Blocked Domain Manager ────────────────────────────────────
        tab2 = QWidget(); t2l = QVBoxLayout()

        info = QLabel(
            "Manage which domains are blocked.\n"
            "🔒 Built-in = hardcoded in network_interceptor.py (always active)\n"
            "👤 User-added = domains YOU added (saved to ~/.mybrowser/security/blocked_domains.json)\n"
            "You can remove built-in domains for this session, or add your own below."
        )
        info.setWordWrap(True)
        info.setStyleSheet(
            "background:rgba(255,255,255,0.07);padding:10px;"
            "border-radius:8px;font-size:12px;")
        t2l.addWidget(info)

        all_blocked = self.network_interceptor.get_all_blocked()
        count_lbl = QLabel(f"Total blocked domains: {len(all_blocked)}")
        count_lbl.setStyleSheet("font-weight:bold;padding:4px;")
        t2l.addWidget(count_lbl)

        domain_list = QListWidget()
        domain_list.setStyleSheet(
            "QListWidget{background:#12122a;color:white;border-radius:6px;}"
            "QListWidget::item{padding:5px;border-bottom:1px solid #2a2a4a;}"
            "QListWidget::item:selected{background:#2a2a5a;}")
        for d in all_blocked:
            tag = "🔒" if self.network_interceptor.is_default_domain(d) else "👤"
            item = QListWidgetItem(f"{tag}  {d}")
            item.setData(Qt.ItemDataRole.UserRole, d)
            domain_list.addItem(item)
        t2l.addWidget(domain_list)

        # Add new domain
        add_row = QHBoxLayout()
        new_domain_input = QLineEdit()
        new_domain_input.setPlaceholderText("Enter domain to block e.g. ads.example.com")
        new_domain_input.setStyleSheet(
            "background:#1e1e3a;color:white;padding:8px;border-radius:6px;font-size:13px;")
        add_row.addWidget(new_domain_input)

        add_btn = QPushButton("➕ Add Domain")
        add_btn.setStyleSheet(
            "background:#2ecc71;color:white;padding:8px 16px;border-radius:6px;font-weight:bold;")
        def add_domain():
            d = new_domain_input.text().strip().lower()
            if not d:
                return
            self.network_interceptor.add_blocked_domain(d)
            tag = "👤"
            item = QListWidgetItem(f"{tag}  {d}")
            item.setData(Qt.ItemDataRole.UserRole, d)
            domain_list.addItem(item)
            count_lbl.setText(f"Total blocked domains: {len(self.network_interceptor.get_all_blocked())}")
            new_domain_input.clear()
        add_btn.clicked.connect(add_domain)
        new_domain_input.returnPressed.connect(add_domain)
        add_row.addWidget(add_btn)
        t2l.addLayout(add_row)

        # Remove selected
        b2 = QHBoxLayout()
        rem_btn = QPushButton("🗑️ Remove Selected")
        rem_btn.setStyleSheet("background:#e74c3c;color:white;padding:8px 16px;border-radius:6px;")
        def remove_domain():
            sel = domain_list.currentItem()
            if not sel:
                return
            d = sel.data(Qt.ItemDataRole.UserRole)
            reply = QMessageBox.question(
                dlg, "Remove Domain",
                f"Remove '{d}' from block list?\n"
                + ("(Built-in — only removed for this session)" if self.network_interceptor.is_default_domain(d) else "(User-added — permanently removed)"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.network_interceptor.remove_blocked_domain(d)
                domain_list.takeItem(domain_list.row(sel))
                count_lbl.setText(f"Total blocked domains: {len(self.network_interceptor.get_all_blocked())}")
        rem_btn.clicked.connect(remove_domain)
        b2.addWidget(rem_btn)

        cls2 = QPushButton("✖ Close")
        cls2.setStyleSheet("background:#555;color:white;padding:8px 16px;border-radius:6px;")
        cls2.clicked.connect(dlg.close)
        b2.addWidget(cls2)
        t2l.addLayout(b2)
        tab2.setLayout(t2l)
        tabs.addTab(tab2, f"🚫 Blocked Domains ({len(all_blocked)})")

        main_lay.addWidget(tabs)
        _central = QWidget(); _central.setLayout(main_lay)
        dlg.setCentralWidget(_central)
        dlg.show()
    def _show_ip_masking(self):
        """
        IP MASKING — what you will see:
        ┌─────────────────────────────────────────────────────────────┐
        │  🔴 Real IP:    192.168.1.100   ← your device's LAN IP      │
        │  🟢 Masked IP:  87.123.45.231   ← mathematically transformed│
        │  ⚙️  Algorithm: simple_hash                                   │
        │  📊 Status:     🟢 Active                                    │
        ├─────────────────────────────────────────────────────────────┤
        │  [simple_hash ▼]  [✅ Apply]  [🚫 Disable]                  │
        └─────────────────────────────────────────────────────────────┘
        ALGORITHMS:
          simple_hash   → SHA256(ip) gives a completely different IP
          xor_mask      → ip XOR 0x12345678 flips specific bits
          random_subnet → keeps 192.168.x.x, randomises last number
          rotate_octets → 192.168.1.100 becomes 100.192.168.1
        ⚠️  This is a DISPLAY demonstration, not a real VPN.
        """
        if not self.ip_masking:
            return
        from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
            QComboBox, QPushButton, QGroupBox, QFormLayout, QHBoxLayout)
        from PyQt6.QtGui import QFont

        dlg = QMainWindow()
        dlg.setWindowTitle("🎭 IP Masking Monitor")
        dlg.setGeometry(300, 180, 560, 540)
        dlg.setStyleSheet("background:#0f0f23; color:white;")
        lay = QVBoxLayout(); lay.setSpacing(10)

        note = QLabel(
            "🎭  IP Masking transforms your IP address mathematically.\n"
            "Real IP = your device's actual network address.\n"
            "Masked IP = a transformed version, calculated in the browser.\n"
            "⚠️  This is a UI demonstration — it does NOT route traffic differently.\n"
            "   For true anonymity use a VPN or Tor Browser."
        )
        note.setWordWrap(True)
        note.setStyleSheet(
            "background:rgba(255,165,0,0.1);padding:12px;border-radius:8px;"
            "border:1px solid rgba(255,165,0,0.3);font-size:12px;")
        lay.addWidget(note)

        grp = QGroupBox("📡 Current Status")
        grp.setStyleSheet(
            "QGroupBox{font-weight:bold;color:white;"
            "border:1px solid #444;border-radius:8px;margin-top:8px;padding-top:8px;}")
        fl = QFormLayout()
        st = self.ip_masking.get_status()

        rl = QLabel(st['original_ip'])
        rl.setStyleSheet(
            "font-family:'Courier New';font-size:14px;color:#ff6b6b;"
            "background:rgba(255,0,0,0.08);padding:4px 8px;border-radius:4px;")
        fl.addRow("🔴 Real IP:", rl)

        ml = QLabel(st['masked_ip'] or '(not enabled yet)')
        ml.setStyleSheet(
            "font-family:'Courier New';font-size:14px;color:#51cf66;"
            "background:rgba(0,255,0,0.08);padding:4px 8px;border-radius:4px;")
        fl.addRow("🟢 Masked IP:", ml)

        al = QLabel(st['algorithm'])
        al.setStyleSheet("color:#74c0fc;")
        fl.addRow("⚙️  Algorithm:", al)
        fl.addRow("📊 Status:", QLabel('🟢 Active' if st['enabled'] else '⚫ Disabled'))
        grp.setLayout(fl); lay.addWidget(grp)

        agrp = QGroupBox("🔧 Change Algorithm")
        agrp.setStyleSheet(
            "QGroupBox{font-weight:bold;color:white;"
            "border:1px solid #444;border-radius:8px;margin-top:8px;padding-top:8px;}")
        aly = QVBoxLayout()
        cb = QComboBox()
        cb.addItems(self.ip_masking.get_algorithms())
        cb.setCurrentText(st['algorithm'])
        cb.setStyleSheet("background:#2a2a4a;color:white;padding:6px;border-radius:6px;")

        descs = {
            'simple_hash':   'SHA256(your_ip) → completely different IP',
            'xor_mask':      'your_ip XOR 0x12345678 → bit-flipped IP',
            'random_subnet': 'Keep 192.168.x.x, randomise last octet',
            'rotate_octets': '192.168.1.100 → 100.192.168.1'
        }
        exp = QLabel(descs.get(st['algorithm'], ''))
        exp.setStyleSheet("color:#aaa;font-size:11px;padding:4px;")
        cb.currentTextChanged.connect(lambda t: exp.setText(descs.get(t, '')))
        aly.addWidget(cb); aly.addWidget(exp)

        brow = QHBoxLayout()
        ab = QPushButton("✅ Apply Masking")
        ab.setStyleSheet(
            "background:#2ecc71;color:white;padding:9px 16px;"
            "border-radius:7px;font-weight:bold;")
        ab.clicked.connect(lambda: [
            self.ip_masking.apply_masking(cb.currentText()), dlg.close()])
        brow.addWidget(ab)
        db = QPushButton("🚫 Disable")
        db.setStyleSheet("background:#e74c3c;color:white;padding:9px 16px;border-radius:7px;")
        db.clicked.connect(lambda: [self.ip_masking.disable_masking(), dlg.close()])
        brow.addWidget(db)
        aly.addLayout(brow)
        agrp.setLayout(aly); lay.addWidget(agrp)
        _central = QWidget(); _central.setLayout(lay); dlg.setCentralWidget(_central); dlg.show()

    # ── Security Dashboard ────────────────────────────────────────
    def _show_security_dashboard(self):
        """
        SECURITY DASHBOARD — what you will see:
        ┌─────────────────────────────────────────────────────────────┐
        │  Security Score: 95%   Grade: A                             │
        │  [███████████████░░░] 95%                                   │
        │  ✅ Excellent — your browser is well protected               │
        ├──────────────────┬──────────┬──────────────────────────────┤
        │ Check             │ Result   │ Details                      │
        │ Recent Threats    │ ✓ PASS   │ 0 high-severity alerts       │
        │ Threat Level      │ ✓ PASS   │ Current level: LOW           │
        ├─────────────────────────────────────────────────────────────┤
        │ Total Alerts: 3  |  Threat Level: LOW                       │
        └─────────────────────────────────────────────────────────────┘
        GRADES:  A=Excellent  B=Good  C=Fair  D=Poor  F=Critical
        THREAT LEVEL rises when the Network Monitor blocks many
        high-priority trackers or detects repeated suspicious requests.
        """
        if not self.security_monitor:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Security Dashboard", "Security monitor not available.")
            return
        from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
            QTableWidget, QTableWidgetItem, QProgressBar,
            QPushButton, QHeaderView)
        from PyQt6.QtGui import QFont, QColor

        try:
            self.security_dashboard_window = QMainWindow()
            dlg = self.security_dashboard_window
            dlg.setWindowTitle("🛡️ Security Dashboard")
            dlg.setGeometry(120, 120, 820, 620)
            dlg.setStyleSheet("background:#0f0f23; color:white;")
            lay = QVBoxLayout(); lay.setSpacing(8)

            hdr = QLabel(
                "🛡️  Security Dashboard — your browser's health report.\n"
                "Each check analyses recent browser activity and rates your safety.\n"
                "Grade A = excellent · B = good · C = fair · D = poor · F = critical\n"
                "Alerts are generated by the Network Monitor when trackers are blocked."
            )
            hdr.setWordWrap(True)
            hdr.setStyleSheet(
                "background:rgba(255,255,255,0.07);padding:10px;"
                "border-radius:8px;font-size:12px;")
            lay.addWidget(hdr)

            res = self.security_monitor.run_security_check(self.network_interceptor)
            gc = {'A':'#2ecc71','B':'#27ae60','C':'#f39c12','D':'#e67e22','F':'#e74c3c'}
            col = gc.get(res['grade'], '#999')

            sl = QLabel(f"Security Score: {res['score']:.0f}%   Grade: {res['grade']}")
            sl.setFont(QFont("Arial", 18, QFont.Weight.Bold))
            sl.setStyleSheet(
            f"color:{col};padding:12px;background:rgba(255,255,255,0.05);border-radius:8px;")
            lay.addWidget(sl)

            pb = QProgressBar(); pb.setValue(int(res['score'])); pb.setFixedHeight(22)
            pb.setStyleSheet(
                f"QProgressBar{{background:rgba(255,255,255,0.1);border-radius:11px;"
                f"color:white;text-align:center;}}"
                f"QProgressBar::chunk{{background:{col};border-radius:11px;}}")
            lay.addWidget(pb)

            gd = {'A':'✅ Excellent — well protected',
                'B':'🟡 Good — minor issues',
                'C':'⚠️  Fair — some threats detected',
                'D':'🔴 Poor — several threats, take action',
                'F':'🚨 Critical — immediate attention needed'}
            gl = QLabel(gd.get(res['grade'], ''))
            gl.setStyleSheet(f"color:{col};font-size:13px;padding:4px;")
            lay.addWidget(gl)

            chks = res['checks']
            tbl = QTableWidget(len(chks), 3)
            tbl.setHorizontalHeaderLabels(["Security Check", "Result", "Details"])
            tbl.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            tbl.setColumnWidth(0, 200); tbl.setColumnWidth(1, 100)
            tbl.setStyleSheet(
                "QTableWidget{background:#12122a;color:white;gridline-color:#2a2a4a;}"
                "QHeaderView::section{background:#2a2a4a;color:white;padding:6px;}")
            for i, c in enumerate(chks):
                tbl.setItem(i, 0, QTableWidgetItem(c['name']))
                si = QTableWidgetItem('✓ PASS' if c['passed'] else '✗ FAIL')
                si.setForeground(QColor('#51cf66') if c['passed'] else QColor('#ff6b6b'))
                tbl.setItem(i, 1, si)
                tbl.setItem(i, 2, QTableWidgetItem(c['message']))
            lay.addWidget(tbl)

            st = self.security_monitor.get_stats()
            tc = {'LOW':'#2ecc71','MEDIUM':'#f39c12','HIGH':'#e74c3c','CRITICAL':'#c0392b'}
            ftxt = (f"📋 Total Alerts: {st['total_alerts']}   |   "
                    f"Threat Level: {st['current_threat_level']}")
            fl = QLabel(ftxt)
            fl.setStyleSheet(
                f"padding:10px;background:rgba(255,255,255,0.05);"
                f"border-radius:6px;color:{tc.get(st['current_threat_level'],'#fff')};")
            lay.addWidget(fl)

            # ── Recent security alerts ─────────────────────────────────
            recent_alerts = self.security_monitor.get_recent_alerts(20)
            from PyQt6.QtWidgets import QListWidget, QListWidgetItem
            from PyQt6.QtGui import QColor as QColorAlert
            al_lbl = QLabel(f"📋 Recent Alerts ({len(recent_alerts)}) — live as you browse")
            al_lbl.setStyleSheet("font-weight:bold;padding:4px;margin-top:4px;")
            lay.addWidget(al_lbl)
            if recent_alerts:
                al_list = QListWidget()
                al_list.setMaximumHeight(120)
                al_list.setStyleSheet(
                    "QListWidget{background:#12122a;color:white;border-radius:6px;}"
                    "QListWidget::item{padding:4px;border-bottom:1px solid #2a2a4a;font-size:11px;}")
                lvl_col = {'LOW':'#51cf66','MEDIUM':'#ffd43b','HIGH':'#ff6b6b','CRITICAL':'#ff4444'}
                for a in reversed(recent_alerts):
                    ico = {'LOW':'🟢','MEDIUM':'🟡','HIGH':'🔴','CRITICAL':'🚨'}.get(a['level'],'⚠️')
                    item = QListWidgetItem(f"{ico}  {a['timestamp'][11:19]}  [{a['category']}]  {a['message']}")
                    item.setForeground(QColorAlert(lvl_col.get(a['level'],'#fff')))
                    al_list.addItem(item)
                lay.addWidget(al_list)
            else:
                no_al = QLabel("No alerts yet — browse websites to see real threat detection. Blocked ads/trackers appear here.")
                no_al.setWordWrap(True)
                no_al.setStyleSheet("color:#888;font-size:12px;padding:6px;")
                lay.addWidget(no_al)

            cb = QPushButton("✖ Close")
            cb.setStyleSheet("background:#555;color:white;padding:8px 16px;border-radius:6px;")
            cb.clicked.connect(dlg.close)
            lay.addWidget(cb)
            _central = QWidget()
            _central.setLayout(lay)
            dlg.setCentralWidget(_central)
            dlg.show()
        except Exception as e:
            import traceback
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Security Dashboard Error", 
                f"Failed to open Security Dashboard:\n{e}\n\n{traceback.format_exc()[-500:]}")

    # ── P2P Send ──────────────────────────────────────────────────
    def _show_p2p_send(self):
        """
        P2P SEND — how it works:
        1. You pick a file on your computer
        2. Your IP address + port 9876 is shown on screen
        3. Tell the receiver your IP (e.g. 192.168.1.100) and port 9876
        4. Receiver opens Security → P2P Receive, enters your IP + port
        5. File transfers DIRECTLY — no cloud, no upload, no server
        Requires both computers to be on the same WiFi/LAN network.
        """
        from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
            QPushButton, QFileDialog, QProgressBar, QHBoxLayout)

        dlg = QMainWindow()
        dlg.setWindowTitle("📡 P2P Send File")
        dlg.setGeometry(280, 180, 520, 460)
        dlg.setStyleSheet("background:#0f0f23; color:white;")
        lay = QVBoxLayout(); lay.setSpacing(8)

        desc = QLabel(
            "📡  P2P Send — transfer a file directly to another computer.\\n"
            "HOW IT WORKS:\n"
            "1️⃣  Choose the file you want to send below\n"
            "2️⃣  Your IP address and port will be shown\n"
            "3️⃣  Share those details with the receiver (verbally / message)\n"
            "4️⃣  Ask them to open  Security → P2P Receive File  and enter your IP\n"
            "5️⃣  File transfers instantly — no cloud service involved!\\n"
            "⚠️  Both computers must be on the same WiFi or LAN network."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet(
            "background:rgba(255,255,255,0.07);padding:12px;border-radius:8px;font-size:12px;")
        lay.addWidget(desc)

        file_lbl = QLabel("No file selected")
        file_lbl.setStyleSheet(
            "color:#74c0fc;padding:8px;background:rgba(255,255,255,0.05);border-radius:6px;")
        lay.addWidget(file_lbl)

        choose_btn = QPushButton("📁  Choose File to Send")
        choose_btn.setStyleSheet(
            "background:#3498db;color:white;padding:10px;border-radius:8px;"
            "font-size:13px;font-weight:bold;")
        selected = [None]

        def pick():
            import os
            p, _ = QFileDialog.getOpenFileName(dlg, "Select File")
            if p:
                selected[0] = p
                sz = os.path.getsize(p) / (1024*1024)
                file_lbl.setText(f"📄  {os.path.basename(p)}  ({sz:.2f} MB)")
        choose_btn.clicked.connect(pick)
        lay.addWidget(choose_btn)

        my_ip = self.ip_masking.get_real_ip() if self.ip_masking else "unknown"
        PORT = 9876
        conn_lbl = QLabel(
            f"📡  Give these details to the receiver:\n"
            f"    IP Address:  {my_ip}\n"
            f"    Port:        {PORT}")
        conn_lbl.setStyleSheet(
            "font-family:'Courier New';font-size:13px;"
            "background:rgba(0,255,0,0.07);padding:12px;border-radius:8px;")
        lay.addWidget(conn_lbl)

        pb = QProgressBar(); pb.setValue(0)
        pb.setStyleSheet(
            "QProgressBar{background:rgba(255,255,255,0.1);border-radius:8px;}"
            "QProgressBar::chunk{background:#2ecc71;border-radius:8px;}")
        lay.addWidget(pb)
        status_lbl = QLabel("Ready — choose a file then click Send")
        status_lbl.setStyleSheet("color:#aaa;font-size:12px;")
        lay.addWidget(status_lbl)

        send_btn = QPushButton("🚀  Start Sending  (waits for receiver to connect)")
        send_btn.setStyleSheet(
            "background:#2ecc71;color:white;padding:10px;border-radius:8px;"
            "font-size:13px;font-weight:bold;")

        def start():
            import os
            if not selected[0]:
                status_lbl.setText("⚠️  Please choose a file first!"); return
            fpath = selected[0]; fsize = os.path.getsize(fpath)
            status_lbl.setText("⏳  Waiting for receiver to connect  (2-min timeout)…")
            send_btn.setEnabled(False)

            def worker():
                try:
                    import socket as s
                    srv = s.socket(s.AF_INET, s.SOCK_STREAM)
                    srv.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
                    srv.bind(('0.0.0.0', PORT)); srv.listen(1); srv.settimeout(120)
                    conn, addr = srv.accept()
                    status_lbl.setText(f"✅  Connected to {addr[0]}!  Sending…")
                    fname = os.path.basename(fpath).encode()
                    conn.sendall(f"{len(fname)}:{fname.decode()}:{fsize}:".encode())
                    sent = 0
                    with open(fpath,'rb') as f:
                        while True:
                            chunk = f.read(65536)
                            if not chunk: break
                            conn.sendall(chunk); sent += len(chunk)
                            pct = int(sent/fsize*100); pb.setValue(pct)
                            status_lbl.setText(
                                f"Sending… {sent//(1024*1024)} / "
                                f"{fsize//(1024*1024)} MB  ({pct}%)")
                    conn.close(); srv.close()
                    status_lbl.setText("✅  File sent successfully!")
                    pb.setValue(100)
                except Exception as e:
                    status_lbl.setText(f"❌  {e}"); send_btn.setEnabled(True)
            import threading
            threading.Thread(target=worker, daemon=True).start()

        send_btn.clicked.connect(start); lay.addWidget(send_btn)
        cls = QPushButton("✖ Close")
        cls.setStyleSheet("background:#555;color:white;padding:8px;border-radius:6px;")
        cls.clicked.connect(dlg.close); lay.addWidget(cls)
        _central = QWidget(); _central.setLayout(lay); dlg.setCentralWidget(_central); dlg.show()

    # ── P2P Receive ───────────────────────────────────────────────
    def _show_p2p_receive(self):
        """
        P2P RECEIVE — how it works:
        1. Sender opens Security → P2P Send File and picks a file
        2. Sender tells you their IP address (e.g. 192.168.1.100) and port 9876
        3. You type that IP and port here and click Receive
        4. Choose a folder to save the file
        5. File downloads directly from the sender's computer
        """
        from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
            QPushButton, QFileDialog, QProgressBar, QLineEdit, QHBoxLayout)

        dlg = QMainWindow()
        dlg.setWindowTitle("📥 P2P Receive File")
        dlg.setGeometry(280, 180, 520, 460)
        dlg.setStyleSheet("background:#0f0f23; color:white;")
        lay = QVBoxLayout(); lay.setSpacing(8)

        desc = QLabel(
            "📥  P2P Receive — download a file directly from another computer.\\n"
            "HOW IT WORKS:\n"
            "1️⃣  Ask the sender to open  Security → P2P Send File\n"
            "2️⃣  The sender picks a file — their IP and port appear on screen\n"
            "3️⃣  Enter their IP Address and Port below\n"
            "4️⃣  Click Receive — choose a save folder — file downloads!\\n"
            "⚠️  Both computers must be on the same WiFi or LAN network."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet(
            "background:rgba(255,255,255,0.07);padding:12px;border-radius:8px;font-size:12px;")
        lay.addWidget(desc)

        inp_style = ("background:#1e1e3a;color:white;padding:9px;"
                     "border-radius:7px;font-size:13px;")
        r1 = QHBoxLayout()
        r1.addWidget(QLabel("Sender IP:"))
        ip_in = QLineEdit(); ip_in.setPlaceholderText("e.g. 192.168.1.100")
        ip_in.setStyleSheet(inp_style); r1.addWidget(ip_in); lay.addLayout(r1)

        r2 = QHBoxLayout()
        r2.addWidget(QLabel("Port:     "))
        pt_in = QLineEdit(); pt_in.setText("9876")
        pt_in.setStyleSheet(inp_style); r2.addWidget(pt_in); lay.addLayout(r2)

        pb = QProgressBar(); pb.setValue(0)
        pb.setStyleSheet(
            "QProgressBar{background:rgba(255,255,255,0.1);border-radius:8px;}"
            "QProgressBar::chunk{background:#3498db;border-radius:8px;}")
        lay.addWidget(pb)
        status_lbl = QLabel("Enter sender IP and click Receive")
        status_lbl.setStyleSheet("color:#aaa;font-size:12px;")
        lay.addWidget(status_lbl)

        recv_btn = QPushButton("📥  Receive File")
        recv_btn.setStyleSheet(
            "background:#3498db;color:white;padding:10px;border-radius:8px;"
            "font-size:13px;font-weight:bold;")

        def start():
            sip = ip_in.text().strip()
            try: sport = int(pt_in.text().strip())
            except: status_lbl.setText("⚠️  Invalid port"); return
            if not sip: status_lbl.setText("⚠️  Enter sender IP"); return
            save_dir = QFileDialog.getExistingDirectory(dlg, "Choose Save Folder")
            if not save_dir: return
            recv_btn.setEnabled(False)
            status_lbl.setText(f"🔗  Connecting to {sip}:{sport}…")

            def worker():
                import socket as s, os
                fname = None
                fsize = 0
                try:
                    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
                    sock.settimeout(30); sock.connect((sip, sport))
                    buf = b""
                    while True:
                        b = sock.recv(1)
                        if not b: break
                        buf += b
                        parts = buf.split(b":")
                        if len(parts) >= 4:
                            try:
                                fname = parts[1].decode(); fsize = int(parts[2]); break
                            except: pass
                    if not fname or fsize == 0:
                        QTimer.singleShot(0, lambda: status_lbl.setText("❌  Bad header from sender"))
                        QTimer.singleShot(0, lambda: recv_btn.setEnabled(True))
                        return
                    _fn, _sz = fname, fsize
                    QTimer.singleShot(0, lambda: status_lbl.setText(
                        f"📥  Receiving {_fn}  ({_sz//(1024*1024)} MB)…"))
                    save_path = os.path.join(save_dir, fname)
                    rcvd = 0
                    with open(save_path, 'wb') as f:
                        while rcvd < fsize:
                            data = sock.recv(65536)
                            if not data: break
                            f.write(data); rcvd += len(data)
                            pct = int(rcvd / fsize * 100)
                            _r, _t, _p = rcvd, fsize, pct
                            QTimer.singleShot(0, lambda v=_p: pb.setValue(v))
                            QTimer.singleShot(0, lambda r=_r, t=_t, p=_p: status_lbl.setText(
                                f"Receiving… {r//(1024*1024)} / {t//(1024*1024)} MB  ({p}%)"))
                    sock.close()
                    _sp = save_path
                    QTimer.singleShot(0, lambda: pb.setValue(100))
                    QTimer.singleShot(0, lambda: status_lbl.setText(f"✅  Saved to: {_sp}"))
                except Exception as e:
                    _e = str(e)
                    QTimer.singleShot(0, lambda: status_lbl.setText(f"❌  {_e}"))
                    QTimer.singleShot(0, lambda: recv_btn.setEnabled(True))
            import threading
            threading.Thread(target=worker, daemon=True).start()

        recv_btn.clicked.connect(start); lay.addWidget(recv_btn)
        cls = QPushButton("✖ Close")
        cls.setStyleSheet("background:#555;color:white;padding:8px;border-radius:6px;")
        cls.clicked.connect(dlg.close); lay.addWidget(cls)
        _central = QWidget(); _central.setLayout(lay); dlg.setCentralWidget(_central); dlg.show()


    # ════════════════════════════════════════════════════════════
    #  CHATBOT FILE / IMAGE ATTACHMENT  (Python-side, works properly)
    #  These use native QFileDialog then inject via runJavaScript()
    #  Called from the chat toolbar buttons added in create_modern_navigation_bar
    # ════════════════════════════════════════════════════════════

    def _chat_attach_image(self):
        """🖼️ Image attach — native file picker → injects into chatbot via JS"""
        import base64, mimetypes, json as _json
        path, _ = QFileDialog.getOpenFileName(
            self, "Attach Image to Chat",
            os.path.expanduser("~"),
            "Images (*.png *.jpg *.jpeg *.gif *.webp *.bmp)"
        )
        if not path:
            return
        try:
            fsize = os.path.getsize(path)
            # Warn for images > 1 MB — Qt's runJavaScript is reliable up to ~1.5 MB of JS.
            if fsize > 1 * 1024 * 1024:
                reply = QMessageBox.question(
                    self, "Large Image",
                    f"This image is {fsize // 1024} KB.\n"
                    "Images over 1 MB may be slow to inject. Continue?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply != QMessageBox.StandardButton.Yes:
                    return

            mime = mimetypes.guess_type(path)[0] or 'image/png'
            with open(path, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode()
            data_url = "data:" + mime + ";base64," + b64
            fname    = os.path.basename(path)
            size_kb  = round(fsize / 1024, 1)

            # json.dumps produces a valid JS string literal for ANY filename
            fname_js     = _json.dumps(fname)
            dataurl_js   = _json.dumps(data_url)
            preview_html = _json.dumps(
                f'\U0001f5bc\ufe0f <strong style="color:#74c0fc">{fname}</strong>'
                f' <span style="color:#aaa">({size_kb}\u00a0KB)</span>'
            )
            js = (
                "(function(){"
                f"window._attachedFile={{name:{fname_js},size:{fsize},"
                f"type:'image',content:null,dataUrl:{dataurl_js}}};"
                "window.attachedFile=window._attachedFile;"
                "var p=document.getElementById('attachPreview');"
                "if(p){"
                f"p.style.display='flex';p.innerHTML={preview_html}"
                "+'<button onclick=\"window._attachedFile=null;window.attachedFile=null;"
                "this.parentElement.style.display=\\'none\\'\" "
                "style=\"margin-left:auto;background:rgba(255,107,107,.2);border:1px solid "
                "#ff6b6b;color:#ff6b6b;border-radius:4px;padding:2px 8px;cursor:pointer;"
                "font-size:11px\">\u2715 Remove</button>';}"
                "var inp=document.getElementById('chatInput');"
                "if(inp){inp.placeholder='Ask about the image\u2026';inp.focus();}"
                "})();"
            )
            self._run_chat_js(js)
            self.statusBar().showMessage(f"✅ Image attached: {fname}", 3000)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not attach image:\n{e}")

    def _chat_attach_file(self):
        """📎 File attach — reads text files and injects into chatbot"""
        import json as _json
        path, _ = QFileDialog.getOpenFileName(
            self, "Attach File to Chat", os.path.expanduser("~"),
            "Text files (*.txt *.py *.js *.ts *.md *.csv *.json *.html *.css "
            "*.xml *.log *.sh *.yaml *.yml);;All files (*)"
        )
        if not path:
            return
        try:
            MAX_READ = 16384  # 16 KB — good context for most LLMs
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                text_content = f.read(MAX_READ)
            fname     = os.path.basename(path)
            fsize     = os.path.getsize(path)
            size_kb   = round(fsize / 1024, 1)
            truncated = fsize > MAX_READ
            note      = ' (first 16 KB)' if truncated else ''

            fname_js     = _json.dumps(fname)
            content_js   = _json.dumps(text_content)
            preview_html = _json.dumps(
                f'\U0001f4ce <strong style="color:#74c0fc">{fname}</strong>'
                f' <span style="color:#aaa">({size_kb}\u00a0KB{note})</span>'
            )
            js = (
                "(function(){"
                f"window._attachedFile={{name:{fname_js},size:{fsize},"
                f"type:'file',content:{content_js},dataUrl:null}};"
                "window.attachedFile=window._attachedFile;"
                "var p=document.getElementById('attachPreview');"
                "if(p){"
                f"p.style.display='flex';p.innerHTML={preview_html}"
                "+'<button onclick=\"window._attachedFile=null;window.attachedFile=null;"
                "this.parentElement.style.display=\\'none\\'\" "
                "style=\"margin-left:auto;background:rgba(255,107,107,.2);border:1px solid "
                "#ff6b6b;color:#ff6b6b;border-radius:4px;padding:2px 8px;cursor:pointer;"
                "font-size:11px\">\u2715 Remove</button>';}"
                "var inp=document.getElementById('chatInput');"
                "if(inp){inp.placeholder='Ask about the file\u2026';inp.focus();}"
                "})();"
            )
            self._run_chat_js(js)
            self.statusBar().showMessage(f"✅ File attached: {fname}", 3000)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not read file:\n{e}")

    def _run_chat_js(self, js):
        """Run JS in the current tab's web page (for chatbot injection)"""
        try:
            widget = self.tabs.currentWidget()
            if widget and hasattr(widget, 'browser'):
                widget.browser.page().runJavaScript(js)
        except Exception as e:
            print(f"runJavaScript error: {e}")
    
    def _setup_attach_polling(self):
        """Poll JS flags for attach button clicks"""
        self._attach_poll_timer = QTimer()
        self._attach_poll_timer.timeout.connect(self._check_attach_flags)
        self._attach_poll_timer.start(200)  # check every 200ms
    
    def _check_attach_flags(self):
        """Check if user clicked attach buttons in chatbot"""
        try:
            widget = self.tabs.currentWidget()
            if not widget or not hasattr(widget, 'browser'):
                return
            # Check image flag
            widget.browser.page().runJavaScript(
                'window._attachImageRequested',
                lambda result: self._handle_image_flag(result) if result else None
            )
            # Check file flag
            widget.browser.page().runJavaScript(
                'window._attachFileRequested',
                lambda result: self._handle_file_flag(result) if result else None
            )
        except Exception:
            pass
    
    def _handle_image_flag(self, requested):
        if requested and not getattr(self, '_attach_busy', False):
            self._reset_flag('_attachImageRequested')
            self._attach_busy = True
            try:
                self._chat_attach_image()
            finally:
                self._attach_busy = False
    
    def _handle_file_flag(self, requested):
        if requested and not getattr(self, '_attach_busy', False):
            self._reset_flag('_attachFileRequested')
            self._attach_busy = True
            try:
                self._chat_attach_file()
            finally:
                self._attach_busy = False
    
    def _reset_flag(self, flag_name):
        """Reset JS flag after handling"""
        try:
            widget = self.tabs.currentWidget()
            if widget and hasattr(widget, 'browser'):
                widget.browser.page().runJavaScript(f'window.{flag_name} = false;')
        except Exception:
            pass

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("My Browser - Privacy Edition")
    app.setFont(QFont("Segoe UI", 10))
    
    window = ModernBrowser()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()