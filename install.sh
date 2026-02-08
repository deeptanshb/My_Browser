#!/bin/bash
# My Browser Installation Script with Ollama AI Integration
# This will set up the browser as a desktop application with AI features

echo "🦕 ========================================"
echo "   MY BROWSER INSTALLATION (AI-ENABLED)"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Create installation directory
INSTALL_DIR="$HOME/mybrowser"
echo -e "${BLUE}📁 Creating installation directory...${NC}"
mkdir -p "$INSTALL_DIR"

# Copy files
echo -e "${BLUE}📋 Copying browser files...${NC}"
cp custom.py "$INSTALL_DIR/" 2>/dev/null || echo -e "${YELLOW}⚠️  custom.py not found${NC}"

# Copy patched version if it exists
if [ -f "custom_patched.py" ]; then
    cp custom_patched.py "$INSTALL_DIR/"
    echo -e "${GREEN}✅ Copied custom_patched.py (Ollama CORS fix)${NC}"
fi

# Copy CORS proxy if it exists
if [ -f "ollama_cors_proxy.py" ]; then
    cp ollama_cors_proxy.py "$INSTALL_DIR/"
    echo -e "${GREEN}✅ Copied ollama_cors_proxy.py${NC}"
fi

# Copy launcher - use enhanced version if available, otherwise use standard
if [ -f "launch_mybrowser_enhanced.py" ]; then
    cp launch_mybrowser_enhanced.py "$INSTALL_DIR/launch_mybrowser.py"
    echo -e "${GREEN}✅ Copied enhanced launcher (with AI support)${NC}"
elif [ -f "launch_mybrowser.py" ]; then
    cp launch_mybrowser.py "$INSTALL_DIR/"
    echo -e "${GREEN}✅ Copied launcher${NC}"
else
    echo -e "${RED}❌ launcher file not found!${NC}"
    exit 1
fi

# Create run.sh launcher
echo -e "${BLUE}🚀 Creating launcher script...${NC}"
cat > "$INSTALL_DIR/run.sh" << 'RUNSCRIPT'
#!/bin/bash
# My Browser Launcher Script with AI Integration
# Keeps terminal open to show any errors

echo "🦕 Starting My Browser..."
echo ""

cd "$(dirname "$0")"

# Check if PyQt6 is installed
python3 -c "import PyQt6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ ERROR: PyQt6 is not installed!"
    echo ""
    echo "Installing PyQt6 using system package manager..."
    echo "This requires sudo privileges."
    echo ""
    
    sudo apt update
    sudo apt install -y python3-pyqt6 python3-pyqt6.qtwebengine
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ Installation failed!"
        echo ""
        echo "Please run manually:"
        echo "  sudo apt install python3-pyqt6 python3-pyqt6.qtwebengine"
        echo ""
        echo "Press Enter to exit..."
        read
        exit 1
    fi
    
    echo ""
    echo "✅ PyQt6 installed successfully!"
    echo ""
fi

# Check for Flask dependencies (for AI features)
python3 -c "import flask, flask_cors, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Flask dependencies not found (needed for AI features)"
    echo "Installing Flask, Flask-CORS, and requests..."
    pip3 install flask flask-cors requests --break-system-packages 2>/dev/null || pip3 install flask flask-cors requests --user
    echo ""
fi

# Run the browser
python3 launch_mybrowser.py

# If there was an error, keep terminal open
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Browser exited with an error"
    echo "Check the log file in ~/.mybrowser/logs/"
    echo ""
    echo "Press Enter to close this window..."
    read
fi
RUNSCRIPT

chmod +x "$INSTALL_DIR/run.sh"

# Create desktop file with correct path
echo -e "${BLUE}🖥️  Creating desktop application...${NC}"
cat > "$HOME/.local/share/applications/mybrowser.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=My Browser 🦕
Comment=Custom Web Browser with AI-Powered Search Assistant
Exec=bash -c "cd $INSTALL_DIR && bash run.sh; exec bash"
Icon=applications-internet
Terminal=true
Categories=Network;WebBrowser;
Keywords=browser;web;internet;dinosaur;ai;ollama;
StartupNotify=true
EOF

chmod +x "$HOME/.local/share/applications/mybrowser.desktop"

# Also create a desktop shortcut
if [ -d "$HOME/Desktop" ]; then
    cp "$HOME/.local/share/applications/mybrowser.desktop" "$HOME/Desktop/"
    chmod +x "$HOME/Desktop/mybrowser.desktop"
    # Try to mark as trusted (for GNOME)
    gio set "$HOME/Desktop/mybrowser.desktop" metadata::trusted true 2>/dev/null || true
    echo -e "${GREEN}✅ Desktop shortcut created${NC}"
fi

# Check if dependencies are installed
echo ""
echo -e "${YELLOW}📦 Checking dependencies...${NC}"

# Check PyQt6
python3 -c "import PyQt6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  PyQt6 not found. Installing using apt...${NC}"
    echo -e "${BLUE}This requires sudo privileges.${NC}"
    echo ""
    sudo apt update
    sudo apt install -y python3-pyqt6 python3-pyqt6.qtwebengine
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ PyQt6 installed successfully${NC}"
    else
        echo -e "${YELLOW}⚠️  Installation failed. You may need to install manually:${NC}"
        echo -e "${YELLOW}   sudo apt install python3-pyqt6 python3-pyqt6.qtwebengine${NC}"
    fi
else
    echo -e "${GREEN}✅ PyQt6 is already installed${NC}"
fi

# Check Flask (for AI features)
python3 -c "import flask, flask_cors, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Flask dependencies not found (needed for AI chatbot)${NC}"
    echo -e "${BLUE}Installing Flask, Flask-CORS, and requests...${NC}"
    pip3 install flask flask-cors requests --break-system-packages 2>/dev/null || pip3 install flask flask-cors requests --user
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Flask dependencies installed${NC}"
    else
        echo -e "${YELLOW}⚠️  Could not install Flask - AI features may not work${NC}"
        echo -e "${YELLOW}   Try: pip3 install flask flask-cors requests${NC}"
    fi
else
    echo -e "${GREEN}✅ Flask dependencies found${NC}"
fi

# Check if Ollama is installed
echo ""
echo -e "${BLUE}🤖 Checking for Ollama...${NC}"
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✅ Ollama is installed${NC}"
    
    # Check if Ollama is running
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Ollama is running${NC}"
        
        # List models
        MODELS=$(curl -s http://localhost:11434/api/tags | python3 -c "import sys, json; data = json.load(sys.stdin); print('\n'.join([m['name'] for m in data.get('models', [])]))" 2>/dev/null)
        
        if [ ! -z "$MODELS" ]; then
            echo -e "${GREEN}✅ Available models:${NC}"
            echo "$MODELS" | while read -r model; do
                echo "   • $model"
            done
        else
            echo -e "${YELLOW}⚠️  No models installed${NC}"
            echo -e "${BLUE}   Install a model: ollama pull mistral${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Ollama is installed but not running${NC}"
        echo -e "${BLUE}   Start Ollama: ollama serve${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Ollama not found${NC}"
    echo -e "${BLUE}   To enable AI chatbot features:${NC}"
    echo -e "${BLUE}   1. Install Ollama: https://ollama.ai${NC}"
    echo -e "${BLUE}   2. Pull a model: ollama pull mistral${NC}"
    echo -e "${BLUE}   3. Start Ollama: ollama serve${NC}"
    echo ""
    echo -e "${YELLOW}   Browser will work without Ollama, but AI chatbot will be in fallback mode${NC}"
fi

# Create logs directory
mkdir -p "$HOME/.mybrowser/logs"

echo ""
echo -e "${GREEN}✅ ========================================"
echo "   INSTALLATION COMPLETE!"
echo "========================================${NC}"
echo ""
echo -e "${BLUE}🦕 Your browser is now installed!${NC}"
echo ""
echo "📁 Installation location: $INSTALL_DIR"
echo "📁 Logs directory: $HOME/.mybrowser/logs"
echo ""

# Show what files were installed
echo -e "${YELLOW}📦 Installed files:${NC}"
ls -1 "$INSTALL_DIR" | sed 's/^/   • /'
echo ""

echo -e "${YELLOW}🚀 HOW TO RUN:${NC}"
echo ""
echo "   Option 1: Search for 'My Browser' in your application menu"
echo "   Option 2: Click the desktop icon (if created)"
echo "   Option 3: Run from terminal: $INSTALL_DIR/run.sh"
echo "   Option 4: Run directly: python3 $INSTALL_DIR/launch_mybrowser.py"
echo ""

if [ -f "$INSTALL_DIR/ollama_cors_proxy.py" ]; then
    echo -e "${GREEN}🤖 AI FEATURES INSTALLED!${NC}"
    echo ""
    echo -e "${BLUE}The browser includes an AI chatbot powered by Ollama.${NC}"
    echo -e "${BLUE}The launcher will automatically:${NC}"
    echo "   • Detect if Ollama is running"
    echo "   • Start the CORS proxy for AI features"
    echo "   • Use the patched browser for seamless AI integration"
    echo ""
    if ! command -v ollama &> /dev/null; then
        echo -e "${YELLOW}⚠️  Install Ollama to enable AI features: https://ollama.ai${NC}"
        echo ""
    fi
fi

echo -e "${BLUE}💡 The terminal window will show monitoring logs while the browser runs${NC}"
echo ""
echo "🦕 Enjoy your custom browser with AI!"
echo ""