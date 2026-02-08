@echo off
REM My Browser Installation Script for Windows
REM This will set up the browser with AI features

title My Browser Installation
color 0B
echo.
echo ========================================
echo    MY BROWSER INSTALLATION (AI-ENABLED)
echo ========================================
echo.

REM Create installation directory
set "INSTALL_DIR=%USERPROFILE%\mybrowser"
echo Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy files
echo.
echo Copying browser files...
if exist "custom.py" (
    copy /Y "custom.py" "%INSTALL_DIR%\" >nul
    echo [OK] Copied custom.py
) else (
    echo [WARNING] custom.py not found
)

if exist "ollama_cors_proxy.py" (
    copy /Y "ollama_cors_proxy.py" "%INSTALL_DIR%\" >nul
    echo [OK] Copied ollama_cors_proxy.py
)

if exist "launch_mybrowser.py" (
    copy /Y "launch_mybrowser.py" "%INSTALL_DIR%\" >nul
    echo [OK] Copied launch_mybrowser.py
) else (
    echo [ERROR] launch_mybrowser.py not found!
    pause
    exit /b 1
)

REM Create run.bat launcher
echo.
echo Creating launcher script...
(
echo @echo off
echo title My Browser
echo cd /d "%%~dp0"
echo.
echo REM Check Python
echo python --version ^>nul 2^>^&1
echo if errorlevel 1 ^(
echo     echo ERROR: Python is not installed!
echo     echo.
echo     echo Please install Python from: https://www.python.org/downloads/
echo     echo Make sure to check "Add Python to PATH" during installation
echo     echo.
echo     pause
echo     exit /b 1
echo ^)
echo.
echo REM Check PyQt6
echo python -c "import PyQt6" ^>nul 2^>^&1
echo if errorlevel 1 ^(
echo     echo Installing PyQt6...
echo     pip install PyQt6 PyQt6-WebEngine
echo ^)
echo.
echo REM Check Flask ^(for AI features^)
echo python -c "import flask, flask_cors, requests" ^>nul 2^>^&1
echo if errorlevel 1 ^(
echo     echo Installing Flask dependencies for AI...
echo     pip install flask flask-cors requests
echo ^)
echo.
echo REM Run browser
echo echo Starting My Browser...
echo python launch_mybrowser.py
echo.
echo if errorlevel 1 ^(
echo     echo.
echo     echo Browser exited with an error
echo     echo Check logs in: %%USERPROFILE%%\.mybrowser\logs\
echo     echo.
echo     pause
echo ^)
) > "%INSTALL_DIR%\run.bat"

echo [OK] Created run.bat

REM Create desktop shortcut using VBScript
echo.
echo Creating desktop shortcut...
set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT=%DESKTOP%\My Browser.lnk"

(
echo Set oWS = WScript.CreateObject^("WScript.Shell"^)
echo sLinkFile = "%SHORTCUT%"
echo Set oLink = oWS.CreateShortcut^(sLinkFile^)
echo oLink.TargetPath = "%INSTALL_DIR%\run.bat"
echo oLink.WorkingDirectory = "%INSTALL_DIR%"
echo oLink.Description = "My Browser - Privacy-focused browser with AI chatbot"
echo oLink.IconLocation = "C:\Windows\System32\shell32.dll,14"
echo oLink.Save
) > "%TEMP%\create_shortcut.vbs"

cscript //nologo "%TEMP%\create_shortcut.vbs" >nul 2>&1
if exist "%SHORTCUT%" (
    echo [OK] Desktop shortcut created
) else (
    echo [WARNING] Could not create desktop shortcut
)
del "%TEMP%\create_shortcut.vbs" >nul 2>&1

REM Check dependencies
echo.
echo ========================================
echo    CHECKING DEPENDENCIES
echo ========================================
echo.

REM Check Python
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    echo After installing Python, run this installer again.
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('python --version') do set PYTHON_VER=%%i
    echo [OK] %PYTHON_VER%
)

REM Check PyQt6
echo Checking PyQt6...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] PyQt6 not found. Installing...
    pip install PyQt6 PyQt6-WebEngine
    if errorlevel 1 (
        echo [ERROR] Failed to install PyQt6
        echo.
        echo Please run manually: pip install PyQt6 PyQt6-WebEngine
        pause
    ) else (
        echo [OK] PyQt6 installed
    )
) else (
    echo [OK] PyQt6 is installed
)

REM Check Flask
echo Checking Flask dependencies...
python -c "import flask, flask_cors, requests" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Flask dependencies not found. Installing...
    pip install flask flask-cors requests
    if errorlevel 1 (
        echo [WARNING] Could not install Flask - AI features may not work
        echo.
        echo Try manually: pip install flask flask-cors requests
    ) else (
        echo [OK] Flask dependencies installed
    )
) else (
    echo [OK] Flask dependencies found
)

REM Check Ollama
echo.
echo Checking for Ollama...
where ollama >nul 2>&1
if errorlevel 1 (
    echo [INFO] Ollama not found
    echo.
    echo To enable AI chatbot features:
    echo   1. Install Ollama from: https://ollama.ai
    echo   2. Pull a model: ollama pull mistral
    echo   3. Start Ollama: ollama serve
    echo.
    echo Browser will work without Ollama, but AI features will be limited.
) else (
    echo [OK] Ollama is installed
    
    REM Check if Ollama is running
    curl -s http://localhost:11434/api/tags >nul 2>&1
    if errorlevel 1 (
        echo [INFO] Ollama is installed but not running
        echo       Start with: ollama serve
    ) else (
        echo [OK] Ollama is running
        REM Try to list models
        echo       Available models:
        curl -s http://localhost:11434/api/tags 2>nul | python -c "import sys, json; [print('       - ' + m['name']) for m in json.load(sys.stdin).get('models', [])]" 2>nul
    )
)

REM Create logs directory
if not exist "%USERPROFILE%\.mybrowser\logs" mkdir "%USERPROFILE%\.mybrowser\logs"

echo.
echo ========================================
echo    INSTALLATION COMPLETE!
echo ========================================
echo.
echo Installation location: %INSTALL_DIR%
echo Logs directory: %USERPROFILE%\.mybrowser\logs
echo.
echo HOW TO RUN:
echo.
echo   Option 1: Double-click "My Browser" icon on desktop
echo   Option 2: Run: %INSTALL_DIR%\run.bat
echo   Option 3: Command: python %INSTALL_DIR%\launch_mybrowser.py
echo.
echo AI FEATURES:
echo   - AI chatbot powered by Ollama
echo   - Code formatting and web search
echo   - Install Ollama for full AI capabilities
echo.
echo Press any key to exit...
pause >nul