"""
Custom Multi-Engine Browser - Advanced Privacy Features
With VPN proxy, secure DNS, search logging, and extensions support
"""
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
        # Ensure the log directory exists
        os.makedirs(log_dir, exist_ok=True)
        self.search_log_file = os.path.join(log_dir, "search_log.txt")
        self.privacy_log_file = os.path.join(log_dir, "privacy_log.json")
        
    def log_search(self, query, engine, timestamp=None):
        """Log a search query"""
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # Text log for easy reading
            with open(self.search_log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] Engine: {engine} | Query: {query}\n")
        except Exception as e:
            print(f"Error writing to search log: {e}")
        
        # JSON log for programmatic access
        try:
            if os.path.exists(self.privacy_log_file):
                with open(self.privacy_log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
        except Exception as e:
            print(f"Error reading privacy log: {e}")
            logs = []
        
        logs.append({
            'timestamp': timestamp,
            'type': 'search',
            'engine': engine,
            'query': query
        })
        
        # Keep only last 10000 entries
        if len(logs) > 10000:
            logs = logs[-10000:]
        
        try:
            with open(self.privacy_log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            print(f"Error writing to privacy log: {e}")
    
    def log_page_visit(self, url, title=""):
        """Log a page visit"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            if os.path.exists(self.privacy_log_file):
                with open(self.privacy_log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
        except Exception as e:
            print(f"Error reading privacy log for page visit: {e}")
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
        
        try:
            with open(self.privacy_log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2)
            print(f"Logged page visit: {url}")  # Debug output
        except Exception as e:
            print(f"Error writing page visit to privacy log: {e}")
    
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
        return """
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
                    padding-right: 50px;
                    border-radius: 20px;
                    word-wrap: break-word;
                    line-height: 1.5;
                    position: relative;
                }
                
                /* Small square copy button */
                .copy-btn {
                    position: absolute;
                    top: 6px;
                    right: 6px;
                    width: 28px;
                    height: 28px;
                    background: rgba(255, 255, 255, 0.15);
                    border: 1px solid rgba(255, 255, 255, 0.25);
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 14px;
                    transition: all 0.2s ease;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    opacity: 0.7;
                    padding: 0;
                }
                
                .copy-btn:hover {
                    background: rgba(255, 255, 255, 0.25);
                    opacity: 1;
                    transform: scale(1.1);
                }
                
                .copy-btn:active {
                    transform: scale(0.95);
                }
                
                .copy-btn.copied {
                    background: rgba(72, 187, 120, 0.9);
                    border-color: rgba(72, 187, 120, 1);
                }
                
                /* Code block copy button */
                .code-block-container {
                    position: relative;
                    margin: 10px 0;
                }
                
                .code-copy-btn {
                    position: absolute;
                    top: 8px;
                    right: 8px;
                    width: 26px;
                    height: 26px;
                    background: rgba(255, 255, 255, 0.12);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 13px;
                    transition: all 0.2s ease;
                    opacity: 0.6;
                    padding: 0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                
                .code-copy-btn:hover {
                    background: rgba(255, 255, 255, 0.22);
                    opacity: 1;
                    transform: scale(1.1);
                }
                
                .code-copy-btn.copied {
                    background: rgba(72, 187, 120, 0.8);
                    border-color: rgba(72, 187, 120, 0.9);
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
                    <div class="quick-link" data-search="news">📰 News</div>
                    <div class="quick-link" data-search="weather">🌤️ Weather</div>
                    <div class="quick-link" data-search="videos">🎬 Videos</div>
                    <div class="quick-link" data-search="images">🖼️ Images</div>
                </div>
                <div class="privacy-badge">🛡️ DNS Protected • Search Logged • Extensions Active</div>
            </div>
            
            <!-- DeepTalks.AI Chatbot -->
            <div class="chatbot-container">
                <div class="chatbot-toggle" id="chatbotToggle">
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
                        <button class="chatbot-close" id="chatbotClose">×</button>
                    </div>
                    
                    <div class="model-indicator" id="modelIndicator">
                        🔄 Connecting to AI Model...
                    </div>
                    
                    <div class="chatbot-messages" id="chatMessages">
                        <div class="message bot">
                            <div class="message-content">
                                👋 Hello! I am DeepTalks.AI, powered by Ollama AI models.
                                
                                <br><br><strong>I can help with:</strong>
                                <br>• Coding & programming
                                <br>• Creative writing & analysis  
                                <br>• General knowledge & explanations
                                
                                <br><br><strong>🌐 For Current Events:</strong>
                                <br>My training data is from 2023. For anything current (2024-2026), I'll:
                                <br>1. Try to get info from Wikipedia (for facts)
                                <br>2. Give you direct search links to Brave/Google (for latest news)
                                
                                <br><br><strong>💡 Pro Tip:</strong> For the freshest info, use the search bar at the top of this browser!
                            </div>
                        </div>
                    </div>
                    
                    <div class="chatbot-input-area">
                        <input type="text" class="chatbot-input" id="chatInput" placeholder="Ask me anything...">
                        <button class="chatbot-send" id="sendBtn">➤</button>
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
                   DeepTalks.AI – FIXED CHATBOT LOGIC
                   ================================ */

                let chatbotOpen = false;
                let conversationHistory = [];
                let currentModel = null;
                let ollamaActive = false;

                /* ---------- Ollama Detection ---------- */
                async function checkOllamaConnection() {
                    try {
                        const response = await fetch('http://localhost:8081/api/tags');
                        if (!response.ok) throw new Error('Ollama not reachable');

                        const data = await response.json();
                        if (data.models && data.models.length > 0) {
                            currentModel = data.models[0].name;
                            ollamaActive = true;
                            updateModelIndicator(`✓ Connected: ${currentModel}`);
                            return true;
                        }
                    } catch (err) {
                        console.warn('[Ollama] Not available:', err.message);
                    }

                    ollamaActive = false;
                    currentModel = null;
                    updateModelIndicator('⚠️ Ollama not running – Limited mode');
                    return false;
                }

                function updateModelIndicator(text) {
                    document.getElementById('modelIndicator').textContent = text;
                }

                /* ---------- UI Controls ---------- */
                // Functions are now attached via event listeners at the end

                /* ---------- Messaging ---------- */
                async function sendMessage() {
                    const input = document.getElementById('chatInput');
                    const message = input.value.trim();
                    if (!message) return;

                    addMessage(message, 'user');
                    conversationHistory.push({ role: 'user', content: message });
                    input.value = '';

                    document.getElementById('sendBtn').disabled = true;
                    showTypingIndicator();

                    try {
                        if (!ollamaActive) await checkOllamaConnection();
                        const reply = await getAIResponse(message);
                        addMessage(reply, 'bot');
                        conversationHistory.push({ role: 'assistant', content: reply });
                    } catch {
                        addMessage('⚠️ Unable to generate a response.', 'bot');
                    }

                    hideTypingIndicator();
                    document.getElementById('sendBtn').disabled = false;
                }

                /* ---------- AI Logic with Web Search ---------- */
                async function getAIResponse(userMessage) {
                    // Check if query needs web search
                    const needsWebSearch = requiresWebSearch(userMessage);
                    let context = '';
                    
                    if (needsWebSearch) {
                        try {
                            const searchResults = await performWebSearch(userMessage);
                            if (searchResults) {
                                context = "\\n\\nCurrent web search results:\\n" + searchResults + "\\n\\nBased on the above information, please answer: ";
                            }
                        } catch (err) {
                            console.error('[Web search error]', err);
                        }
                    }
                    
                    if (ollamaActive) {
                        try {
                            const response = await fetch('http://localhost:8081/api/generate', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    model: currentModel || 'mistral:latest',
                                    prompt: context + userMessage,
                                    stream: false,
                                    system: 'You are DeepTalks.AI, a helpful AI assistant. When provided with web search results, use them to give accurate, current information. IMPORTANT: When writing code, ALWAYS format it properly with code blocks using triple backticks and language name like python or javascript. Put code in separate blocks from explanations. Keep code clean and well-formatted.'
                                })
                            });

                            if (response.ok) {
                                const data = await response.json();
                                if (data.response) return data.response;
                            }
                        } catch (err) {
                            console.error('[Ollama error]', err);
                        }
                    }

                    return generateFallbackResponse(userMessage);
                }
                
                /* ---------- Web Search Detection ---------- */
                function requiresWebSearch(message) {
                    const msg = message.toLowerCase();
                    
                    // Explicit web search request
                    if (msg.includes('search for') || msg.includes('look up') || msg.includes('find info')) {
                        return true;
                    }
                    
                    // Time-sensitive keywords
                    const searchKeywords = [
                        'news', 'current', 'latest', 'today', 'recent', 'now', 'this week', 'this month', 'this year',
                        'weather', 'forecast', 'temperature',
                        'stock', 'price', 'market', 'trading',
                        'what happened', 'breaking', 'update',
                        'score', 'game', 'match', 'tournament', 'championship',
                        'election', 'vote', 'results',
                        'trending', 'viral', 'popular',
                        'when did', 'when was', 'who is currently', 'who won',
                        'schedule', 'event', 'release date',
                        '2024', '2025', '2026'  // Years indicate current events
                    ];
                    
                    return searchKeywords.some(keyword => msg.includes(keyword));
                }
                
                /* ---------- Web Search Function ---------- */
                async function performWebSearch(query) {
                    try {
                        // Try Wikipedia API first for factual information
                        const wikiQuery = encodeURIComponent(query);
                        const wikiResponse = await fetch("https://en.wikipedia.org/api/rest_v1/page/summary/" + wikiQuery);
                        
                        if (wikiResponse.ok) {
                            const wikiData = await wikiResponse.json();
                            
                            if (wikiData.extract && wikiData.extract.length > 50) {
                                let results = "📚 Information from Wikipedia:\\n\\n";
                                results += wikiData.extract + "\\n\\n";
                                
                                if (wikiData.content_urls && wikiData.content_urls.desktop) {
                                    results += "Source: " + wikiData.content_urls.desktop.page + "\\n\\n";
                                }
                                
                                results += "💡 For current news and updates, search directly:\\n";
                                results += "• Brave: https://search.brave.com/search?q=" + wikiQuery + "\\n";
                                results += "• Google: https://www.google.com/search?q=" + wikiQuery;
                                
                                return results;
                            }
                        }
                    } catch (err) {
                        console.log('[Wikipedia search failed, trying direct search]', err);
                    }
                    
                    // If Wikipedia doesn't have it, provide direct search links
                    const searchQuery = encodeURIComponent(query);
                    let results = "🔍 To find current information about: " + query + "\\n\\n";
                    results += "Click these search links for the latest results:\\n\\n";
                    results += "🦁 Brave Search:\\n";
                    results += "   https://search.brave.com/search?q=" + searchQuery + "\\n\\n";
                    results += "🔍 Google Search:\\n";
                    results += "   https://www.google.com/search?q=" + searchQuery + "\\n\\n";
                    results += "🦆 DuckDuckGo:\\n";
                    results += "   https://duckduckgo.com/?q=" + searchQuery + "\\n\\n";
                    results += "💡 Tip: You can also type '" + query + "' in the search bar at the top of this browser!";
                    
                    return results;
                }

                /* ---------- Fallback (HONEST) ---------- */
                function generateFallbackResponse(message) {
                    const msg = message.toLowerCase();

                    if (msg.includes('hello') || msg.includes('hi')) {
                        return ollamaActive
                            ? "Hello! 👋 How can I help you today?"
                            : "Hello! 👋 I am running in limited mode right now.";
                    }

                    if (msg.includes('ollama')) {
                        return "To enable full AI features:\\n\\n1. Install Ollama\\n2. Run: ollama pull mistral\\n3. Start Ollama\\n4. Refresh this page";
                    }

                    return "I am currently running in limited mode. Start Ollama locally to unlock full AI responses.";
                }

                /* ---------- UI Helpers ---------- */
                function addMessage(text, type) {
                    const container = document.getElementById('chatMessages');
                    const msgDiv = document.createElement('div');
                    msgDiv.className = "message " + type;
                    
                    // Format the message content
                    const contentDiv = document.createElement('div');
                    contentDiv.className = 'message-content';
                    
                    // Store original text for copying
                    const originalText = text;
                    
                    // Convert code blocks with copy buttons: ```language\\ncode\\n``` or ```\\ncode\\n```
                    let formatted = text.replace(/```(\\w+)?\\n([\\s\\S]*?)```/g, function(match, lang, code) {
                        const language = lang || 'plaintext';
                        const cleanCode = escapeHtml(code.trim());
                        const codeId = 'code-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
                        return '<div class="code-block-container">' +
                               '<button class="code-copy-btn" data-code-id="' + codeId + '">📋</button>' +
                               '<pre><code id="' + codeId + '" class="language-' + language + '">' + cleanCode + '</code></pre>' +
                               '</div>';
                    });
                    
                    // Convert inline code: `code`
                    formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');
                    
                    // Convert newlines to <br> for non-code text
                    formatted = formatted.replace(/\\n/g, '<br>');
                    
                    // Convert **bold**
                    formatted = formatted.replace(/\\*\\*([^*]+)\\*\\*/g, '<strong>$1</strong>');
                    
                    // Convert bullet points
                    formatted = formatted.replace(/^• /gm, '&nbsp;&nbsp;• ');
                    
                    contentDiv.innerHTML = formatted;
                    
                    // Add copy button for bot messages
                    if (type === 'bot') {
                        const copyBtn = document.createElement('button');
                        copyBtn.className = 'copy-btn';
                        copyBtn.innerHTML = '📋';
                        copyBtn.title = 'Copy message';
                        copyBtn.onclick = function(e) {
                            e.stopPropagation();
                            copyToClipboard(originalText, copyBtn);
                        };
                        contentDiv.appendChild(copyBtn);
                        
                        // Add click handlers to code copy buttons
                        const codeCopyBtns = contentDiv.querySelectorAll('.code-copy-btn');
                        codeCopyBtns.forEach(btn => {
                            btn.onclick = function(e) {
                                e.stopPropagation();
                                const codeId = btn.getAttribute('data-code-id');
                                copyCode(codeId, btn);
                            };
                        });
                    }
                    
                    msgDiv.appendChild(contentDiv);
                    container.appendChild(msgDiv);
                    container.scrollTop = container.scrollHeight;
                }
                
                /* ---------- Linux-Compatible Copy Functions ---------- */
                function copyToClipboard(text, button) {
                    // Remove markdown formatting for plain text copy
                    let cleanText = text
                        .replace(/```[\\w]*\\n/g, '')
                        .replace(/```/g, '')
                        .replace(/\\*\\*([^*]+)\\*\\*/g, '$1')
                        .replace(/`([^`]+)`/g, '$1');
                    
                    // Create temporary textarea (works on Linux)
                    const textarea = document.createElement('textarea');
                    textarea.value = cleanText;
                    textarea.style.position = 'fixed';
                    textarea.style.opacity = '0';
                    document.body.appendChild(textarea);
                    textarea.select();
                    
                    try {
                        const successful = document.execCommand('copy');
                        if (successful) {
                            button.innerHTML = '✓';
                            button.classList.add('copied');
                            setTimeout(() => {
                                button.innerHTML = '📋';
                                button.classList.remove('copied');
                            }, 2000);
                        } else {
                            button.innerHTML = '✗';
                            setTimeout(() => {
                                button.innerHTML = '📋';
                            }, 2000);
                        }
                    } catch (err) {
                        console.error('Copy failed:', err);
                        button.innerHTML = '✗';
                        setTimeout(() => {
                            button.innerHTML = '📋';
                        }, 2000);
                    }
                    
                    document.body.removeChild(textarea);
                }
                
                function copyCode(codeId, button) {
                    const codeElement = document.getElementById(codeId);
                    if (!codeElement) return;
                    
                    const codeText = codeElement.textContent;
                    
                    // Create temporary textarea (works on Linux)
                    const textarea = document.createElement('textarea');
                    textarea.value = codeText;
                    textarea.style.position = 'fixed';
                    textarea.style.opacity = '0';
                    document.body.appendChild(textarea);
                    textarea.select();
                    
                    try {
                        const successful = document.execCommand('copy');
                        if (successful) {
                            button.innerHTML = '✓';
                            button.classList.add('copied');
                            setTimeout(() => {
                                button.innerHTML = '📋';
                                button.classList.remove('copied');
                            }, 2000);
                        } else {
                            button.innerHTML = '✗';
                            setTimeout(() => {
                                button.innerHTML = '📋';
                            }, 2000);
                        }
                    } catch (err) {
                        console.error('Copy failed:', err);
                        button.innerHTML = '✗';
                        setTimeout(() => {
                            button.innerHTML = '📋';
                        }, 2000);
                    }
                    
                    document.body.removeChild(textarea);
                }
                
                function escapeHtml(text) {
                    const div = document.createElement('div');
                    div.textContent = text;
                    return div.innerHTML;
                }

                function showTypingIndicator() {
                    const container = document.getElementById('chatMessages');
                    const div = document.createElement('div');
                    div.className = 'message bot';
                    div.id = 'typingIndicator';
                    div.innerHTML = '<div class="typing-indicator">' +
                        '<div class="typing-dot"></div>' +
                        '<div class="typing-dot"></div>' +
                        '<div class="typing-dot"></div>' +
                        '</div>';
                    container.appendChild(div);
                    container.scrollTop = container.scrollHeight;
                }

                function hideTypingIndicator() {
                    const el = document.getElementById('typingIndicator');
                    if (el) el.remove();
                }
                
                /* ---------- Event Listeners (DOM Ready) ---------- */
                document.addEventListener('DOMContentLoaded', function() {
                    // Chatbot toggle button
                    document.getElementById('chatbotToggle').addEventListener('click', function() {
                        const chatWindow = document.getElementById('chatbotWindow');
                        chatbotOpen = !chatbotOpen;
                        if (chatbotOpen) {
                            chatWindow.classList.add('active');
                            document.getElementById('chatInput').focus();
                            checkOllamaConnection();
                        } else {
                            chatWindow.classList.remove('active');
                        }
                    });
                    
                    // Chatbot close button
                    document.getElementById('chatbotClose').addEventListener('click', function() {
                        document.getElementById('chatbotWindow').classList.remove('active');
                        chatbotOpen = false;
                    });
                    
                    // Send button
                    document.getElementById('sendBtn').addEventListener('click', sendMessage);
                    
                    // Chat input Enter key
                    document.getElementById('chatInput').addEventListener('keypress', function(event) {
                        if (event.key === 'Enter' && !event.shiftKey) {
                            event.preventDefault();
                            sendMessage();
                        }
                    });
                    
                    // Quick links
                    document.querySelectorAll('.quick-link').forEach(link => {
                        link.addEventListener('click', function() {
                            const searchTerm = this.getAttribute('data-search');
                            performSearch(searchTerm);
                        });
                    });
                });
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
        cancel_btn.clicked.connect(self.reject)
        
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
        self.accept()
    
    def view_logs(self):
        log_viewer = SearchLogViewer(self, self.parent_browser.privacy_logger)
        log_viewer.exec()


class SearchLogViewer(QDialog):
    """View search and privacy logs"""
    
    def __init__(self, parent, logger):
        super().__init__(parent)
        self.logger = logger
        self.setWindowTitle("Search & Privacy Logs")
        self.setGeometry(200, 200, 800, 600)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        info = QLabel("📊 Your Browsing & Search History (stored locally for privacy audit)")
        layout.addWidget(info)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        
        # Load ALL logs (searches and page visits)
        try:
            if os.path.exists(self.logger.privacy_log_file):
                with open(self.logger.privacy_log_file, 'r', encoding='utf-8') as f:
                    all_logs = json.load(f)
                    # Get last 200 entries
                    recent_logs = all_logs[-200:] if len(all_logs) > 200 else all_logs
            else:
                recent_logs = []
        except:
            recent_logs = []
        
        log_content = ""
        for log in reversed(recent_logs):
            if log['type'] == 'search':
                log_content += f"[{log['timestamp']}] 🔍 SEARCH on {log['engine']}: {log['query']}\n"
            elif log['type'] == 'visit':
                title = log.get('title', 'Untitled')
                log_content += f"[{log['timestamp']}] 🌐 VISIT: {title}\n    URL: {log['url']}\n"
        
        if not log_content:
            log_content = "No browsing history yet. Start browsing to see your history here!"
        
        self.log_text.setText(log_content)
        layout.addWidget(self.log_text)
        
        btn_layout = QHBoxLayout()
        export_btn = QPushButton("💾 Export Logs")
        export_btn.clicked.connect(self.export_logs)
        clear_btn = QPushButton("🗑️ Clear Logs")
        clear_btn.clicked.connect(self.clear_logs)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        
        btn_layout.addWidget(export_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def export_logs(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export Logs", "", "Text Files (*.txt)")
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.log_text.toPlainText())
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
                self.log_text.clear()
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
        self.extension_manager = ExtensionManager(os.path.join(self.data_dir, "extensions"))
        
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
        q = self.url_bar.text()
        browser = self.current_browser()
        
        if browser:
            if '.' in q and ' ' not in q and not q.startswith('http'):
                url = 'http://' + q
            elif q.startswith('http://') or q.startswith('https://'):
                url = q
            else:
                # Log search
                self.log_search(q)
                
                # Use backend search engine if on My Browser, otherwise use browser's own search
                if self.current_search_engine == 'My Browser':
                    # Get backend search engine from settings
                    backend_engine = self.settings.get('backend_search_engine', 'Brave Search')
                    search_url = SEARCH_ENGINES[backend_engine]['search_url']
                else:
                    # Use the browser's own search URL (Google, Brave, DuckDuckGo)
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
    
    def show_privacy_settings(self):
        dialog = PrivacySettingsDialog(self, self.settings)
        dialog.exec()
        self.update_privacy_indicator()
    
    def show_search_logs(self):
        viewer = SearchLogViewer(self, self.privacy_logger)
        viewer.exec()
    
    def show_extensions(self):
        dialog = ExtensionsDialog(self, self.extension_manager)
        dialog.exec()
    
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
        
        def on_load_finished(success):
            if not success:
                return
                
            title = tab.browser.page().title() if tab.browser else "New Tab"
            url = tab.browser.url().toString() if tab.browser else ""
            
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
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
            print(f"History saved: {len(self.history)} entries")  # Debug output
        except Exception as e:
            print(f"Error saving history: {e}")
    
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
        dialog.exec()
    
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


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("My Browser - Privacy Edition")
    app.setFont(QFont("Segoe UI", 10))
    
    window = ModernBrowser()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()