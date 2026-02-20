#!/bin/bash
# My Browser - Complete Installation Script
# Features: AI Chatbot + Security Microservices
# Supports: Ubuntu/Debian Linux

echo "🦕 ========================================"
echo "   MY BROWSER - COMPLETE INSTALLATION"
echo "   AI + Security Microservices"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Installation directory
INSTALL_DIR="$HOME/mybrowser"
echo -e "${BLUE}📂 Installation directory: $INSTALL_DIR${NC}"
mkdir -p "$INSTALL_DIR"
echo ""

# ============================================
# FILE COPYING
# ============================================

echo -e "${BLUE}📋 Copying files...${NC}"

# Main browser file
if [ -f "custom.py" ]; then
    cp custom.py "$INSTALL_DIR/"
    echo -e "${GREEN}✅ custom.py${NC}"
else
    echo -e "${RED}❌ custom.py not found!${NC}"
    exit 1
fi

# Launcher
if [ -f "launch_mybrowser.py" ]; then
    cp launch_mybrowser.py "$INSTALL_DIR/"
    echo -e "${GREEN}✅ launch_mybrowser.py${NC}"
else
    echo -e "${YELLOW}⚠️  launch_mybrowser.py not found${NC}"
fi

# CORS proxy for AI
if [ -f "ollama_cors_proxy.py" ]; then
    cp ollama_cors_proxy.py "$INSTALL_DIR/"
    echo -e "${GREEN}✅ ollama_cors_proxy.py (for AI chatbot)${NC}"
else
    echo -e "${YELLOW}⚠️  ollama_cors_proxy.py not found - AI features may be limited${NC}"
fi

# Microservices modules
if [ -d "modules" ]; then
    cp -r modules "$INSTALL_DIR/"
    
    # Check which modules are present
    modules_count=0
    [ -f "$INSTALL_DIR/modules/__init__.py" ] && ((modules_count++))
    [ -f "$INSTALL_DIR/modules/network_interceptor.py" ] && ((modules_count++))
    [ -f "$INSTALL_DIR/modules/ip_masking.py" ] && ((modules_count++))
    [ -f "$INSTALL_DIR/modules/social_tabs.py" ] && ((modules_count++))
    [ -f "$INSTALL_DIR/modules/security_monitor.py" ] && ((modules_count++))
    
    if [ $modules_count -eq 5 ]; then
        echo -e "${GREEN}✅ modules/ directory (all $modules_count modules)${NC}"
        echo -e "   ${GREEN}📱 Social Media Tabs${NC}"
        echo -e "   ${GREEN}🎭 IP Masking Monitor${NC}"
        echo -e "   ${GREEN}🌐 Network Interceptor${NC}"
        echo -e "   ${GREEN}🛡️  Security Dashboard${NC}"
    else
        echo -e "${YELLOW}⚠️  modules/ directory (only $modules_count/5 modules found)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  modules/ directory not found - microservices disabled${NC}"
fi

echo ""

# ============================================
# CREATE RUN SCRIPT
# ============================================

echo -e "${BLUE}🚀 Creating launcher script...${NC}"
cat > "$INSTALL_DIR/run.sh" << 'RUNSCRIPT'
#!/bin/bash
# My Browser Complete Edition Launcher

echo "🦕 Starting My Browser - Complete Edition..."
echo ""

cd "$(dirname "$0")"

# Check PyQt6
python3 -c "import PyQt6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ PyQt6 is not installed!"
    echo ""
    echo "Installing PyQt6..."
    sudo apt update
    sudo apt install -y python3-pyqt6 python3-pyqt6.qtwebengine
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ Installation failed!"
        echo "Please run: sudo apt install python3-pyqt6 python3-pyqt6.qtwebengine"
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo "✅ PyQt6 installed!"
    echo ""
fi

# Check Flask (for AI features)
python3 -c "import flask, flask_cors, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Flask dependencies missing (needed for AI chatbot)"
    echo "Installing Flask, Flask-CORS, requests..."
    pip3 install flask flask-cors requests --break-system-packages 2>/dev/null || \
    pip3 install flask flask-cors requests --user
    echo ""
fi

# Run browser
python3 launch_mybrowser.py

# Keep terminal open on error
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Browser exited with an error"
    echo "Check logs in: ~/.mybrowser/logs/"
    echo ""
    read -p "Press Enter to close..."
fi
RUNSCRIPT

chmod +x "$INSTALL_DIR/run.sh"
echo -e "${GREEN}✅ run.sh created${NC}"
echo ""

# ============================================
# CREATE DESKTOP LAUNCHER
# ============================================

echo -e "${BLUE}🖥️  Creating desktop application...${NC}"
mkdir -p "$HOME/.local/share/applications"

cat > "$HOME/.local/share/applications/mybrowser.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=My Browser 🦕
Comment=Privacy Browser with AI Chatbot & Security Tools
Exec=bash -c "cd $INSTALL_DIR && bash run.sh; exec bash"
Icon=applications-internet
Terminal=true
Categories=Network;WebBrowser;
Keywords=browser;web;internet;ai;security;privacy;
StartupNotify=true
EOF

chmod +x "$HOME/.local/share/applications/mybrowser.desktop"
echo -e "${GREEN}✅ Desktop application registered${NC}"

# Create desktop shortcut
if [ -d "$HOME/Desktop" ]; then
    cp "$HOME/.local/share/applications/mybrowser.desktop" "$HOME/Desktop/"
    chmod +x "$HOME/Desktop/mybrowser.desktop"
    gio set "$HOME/Desktop/mybrowser.desktop" metadata::trusted true 2>/dev/null || true
    echo -e "${GREEN}✅ Desktop shortcut created${NC}"
fi
echo ""

# ============================================
# DEPENDENCY CHECKS
# ============================================

echo -e "${YELLOW}📦 Checking dependencies...${NC}"
echo ""

# Check PyQt6
python3 -c "import PyQt6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  PyQt6 not found${NC}"
    echo -e "${BLUE}Installing PyQt6...${NC}"
    sudo apt update
    sudo apt install -y python3-pyqt6 python3-pyqt6.qtwebengine
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ PyQt6 installed${NC}"
    else
        echo -e "${RED}❌ PyQt6 installation failed${NC}"
        echo -e "${YELLOW}   Run manually: sudo apt install python3-pyqt6 python3-pyqt6.qtwebengine${NC}"
    fi
else
    echo -e "${GREEN}✅ PyQt6 installed${NC}"
fi

# Check Flask
python3 -c "import flask, flask_cors, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Flask dependencies missing (for AI chatbot)${NC}"
    echo -e "${BLUE}Installing Flask, Flask-CORS, requests...${NC}"
    pip3 install flask flask-cors requests --break-system-packages 2>/dev/null || \
    pip3 install flask flask-cors requests --user
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Flask dependencies installed${NC}"
    else
        echo -e "${YELLOW}⚠️  Could not install Flask - AI may not work${NC}"
    fi
else
    echo -e "${GREEN}✅ Flask dependencies installed${NC}"
fi

echo ""

# ============================================
# OLLAMA CHECK
# ============================================

echo -e "${BLUE}🤖 Checking for Ollama...${NC}"
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✅ Ollama is installed${NC}"
    
    # Check if running
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Ollama is running${NC}"
        
        # List models
        MODELS=$(curl -s http://localhost:11434/api/tags | \
                 python3 -c "import sys, json; data = json.load(sys.stdin); print('\n'.join([m['name'] for m in data.get('models', [])]))" 2>/dev/null)
        
        if [ ! -z "$MODELS" ]; then
            echo -e "${GREEN}✅ Available AI models:${NC}"
            echo "$MODELS" | while read -r model; do
                echo "   • $model"
            done
        else
            echo -e "${YELLOW}⚠️  No models installed${NC}"
            echo -e "${BLUE}   Install: ollama pull mistral${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Ollama installed but not running${NC}"
        echo -e "${BLUE}   Start: ollama serve${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Ollama not found${NC}"
    echo -e "${BLUE}   To enable AI chatbot:${NC}"
    echo -e "${BLUE}   1. Install: https://ollama.ai${NC}"
    echo -e "${BLUE}   2. Pull model: ollama pull mistral${NC}"
    echo -e "${BLUE}   3. Start: ollama serve${NC}"
    echo ""
    echo -e "${YELLOW}   (Browser works without Ollama, but AI chatbot will be limited)${NC}"
fi

echo ""

# Create logs directory
mkdir -p "$HOME/.mybrowser/logs"

# ============================================
# INSTALLATION COMPLETE
# ============================================

echo -e "${GREEN}✅ ========================================${NC}"
echo -e "${GREEN}   INSTALLATION COMPLETE!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}🦕 My Browser - Complete Edition installed!${NC}"
echo ""
echo -e "📂 Installation: $INSTALL_DIR"
echo -e "📝 Logs: $HOME/.mybrowser/logs"
echo ""

# Show installed files
echo -e "${YELLOW}📦 Installed files:${NC}"
ls -1 "$INSTALL_DIR" | sed 's/^/   • /'
echo ""

# Show microservices status
if [ -d "$INSTALL_DIR/modules" ]; then
    echo -e "${GREEN}🔧 Microservices Status:${NC}"
    [ -f "$INSTALL_DIR/modules/network_interceptor.py" ] && echo -e "   ✅ Network Request Interceptor"
    [ -f "$INSTALL_DIR/modules/ip_masking.py" ] && echo -e "   ✅ IP Masking Monitor"
    [ -f "$INSTALL_DIR/modules/social_tabs.py" ] && echo -e "   ✅ Social Media Quick Tabs"
    [ -f "$INSTALL_DIR/modules/security_monitor.py" ] && echo -e "   ✅ Security Dashboard"
    echo ""
fi

echo -e "${YELLOW}🚀 HOW TO RUN:${NC}"
echo ""
echo "   Option 1: Search 'My Browser' in applications menu"
echo "   Option 2: Click desktop icon"
echo "   Option 3: Terminal: $INSTALL_DIR/run.sh"
echo "   Option 4: Terminal: python3 $INSTALL_DIR/launch_mybrowser.py"
echo ""

echo -e "${BLUE}📋 FEATURES:${NC}"
echo "   ✅ All search engines"
echo "   ✅ Privacy logging & bookmarks"
echo "   ✅ Extensions & downloads"

if [ -f "$INSTALL_DIR/ollama_cors_proxy.py" ]; then
    echo "   ✅ 🤖 AI Chatbot (if Ollama running)"
fi

if [ -d "$INSTALL_DIR/modules" ]; then
    echo "   ✅ 📱 Social Media Quick Tabs"
    echo "   ✅ 🎭 IP Masking Monitor"
    echo "   ✅ 🌐 Network Request Interceptor"
    echo "   ✅ 🛡️  Security Dashboard"
fi

echo ""
echo -e "${BLUE}💡 Terminal shows monitoring logs while browser runs${NC}"
echo ""
echo "🦕 Enjoy your complete browser with AI & security tools!"
echo ""

# Offer to launch
read -p "Launch browser now? (y/n): " launch
if [[ "$launch" == "y" || "$launch" == "Y" ]]; then
    echo ""
    cd "$INSTALL_DIR"
    bash run.sh
fi