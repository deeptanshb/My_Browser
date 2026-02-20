@echo off
:: My Browser - Complete Installation Script (Windows)
:: Features: AI Chatbot + Security Microservices
:: Supports: Windows 10/11

title My Browser - Installation

echo ==================================================
echo    MY BROWSER - COMPLETE INSTALLATION (WINDOWS)
echo    AI + Security Microservices
echo ==================================================
echo.

:: Colors via PowerShell
set "GREEN=[92m"
set "BLUE=[94m"
set "YELLOW=[93m"
set "RED=[91m"
set "NC=[0m"

:: Installation directory
set "INSTALL_DIR=%USERPROFILE%\mybrowser"
echo [94mInstallation directory: %INSTALL_DIR%[0m
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
echo.

:: ============================================
:: FILE COPYING
:: ============================================

echo [94mCopying files...[0m

:: Main browser file
if exist "custom.py" (
    copy /Y "custom.py" "%INSTALL_DIR%\" >nul
    echo [92m  custom.py[0m
) else (
    echo [91m  custom.py not found! Aborting.[0m
    pause
    exit /b 1
)

:: Launcher
if exist "launch_mybrowser.py" (
    copy /Y "launch_mybrowser.py" "%INSTALL_DIR%\" >nul
    echo [92m  launch_mybrowser.py[0m
) else (
    echo [93m  launch_mybrowser.py not found[0m
)

:: CORS proxy for AI
if exist "ollama_cors_proxy.py" (
    copy /Y "ollama_cors_proxy.py" "%INSTALL_DIR%\" >nul
    echo [92m  ollama_cors_proxy.py (for AI chatbot)[0m
) else (
    echo [93m  ollama_cors_proxy.py not found - AI features may be limited[0m
)

:: Microservices modules
if exist "modules\" (
    xcopy /E /I /Y "modules" "%INSTALL_DIR%\modules\" >nul
    echo [92m  modules\ directory copied[0m

    set "modules_count=0"
    if exist "%INSTALL_DIR%\modules\__init__.py"           set /a modules_count+=1
    if exist "%INSTALL_DIR%\modules\network_interceptor.py" set /a modules_count+=1
    if exist "%INSTALL_DIR%\modules\ip_masking.py"         set /a modules_count+=1
    if exist "%INSTALL_DIR%\modules\social_tabs.py"        set /a modules_count+=1
    if exist "%INSTALL_DIR%\modules\security_monitor.py"   set /a modules_count+=1

    echo [92m     Social Media Tabs[0m
    echo [92m     IP Masking Monitor[0m
    echo [92m     Network Interceptor[0m
    echo [92m     Security Dashboard[0m
) else (
    echo [93m  modules\ not found - microservices disabled[0m
)

echo.

:: ============================================
:: CREATE run.bat LAUNCHER
:: ============================================

echo [94mCreating launcher script...[0m

(
echo @echo off
echo title My Browser - Complete Edition
echo echo Starting My Browser - Complete Edition...
echo echo.
echo cd /d "%INSTALL_DIR%"
echo.
echo :: Check PyQt6
echo python -c "import PyQt6" 2^>nul
echo if %%errorlevel%% neq 0 ^(
echo     echo PyQt6 is not installed!
echo     echo Installing PyQt6...
echo     pip install PyQt6 PyQt6-WebEngine
echo     if %%errorlevel%% neq 0 ^(
echo         echo Installation failed! Run manually: pip install PyQt6 PyQt6-WebEngine
echo         pause
echo         exit /b 1
echo     ^)
echo     echo PyQt6 installed!
echo ^)
echo.
echo :: Check Flask
echo python -c "import flask, flask_cors, requests" 2^>nul
echo if %%errorlevel%% neq 0 ^(
echo     echo Flask dependencies missing. Installing...
echo     pip install flask flask-cors requests
echo ^)
echo.
echo :: Run browser
echo python launch_mybrowser.py
echo if %%errorlevel%% neq 0 ^(
echo     echo.
echo     echo Browser exited with an error.
echo     pause
echo ^)
) > "%INSTALL_DIR%\run.bat"

echo [92m  run.bat created[0m
echo.

:: ============================================
:: CREATE DESKTOP SHORTCUT
:: ============================================

echo [94mCreating desktop shortcut...[0m

powershell -NoProfile -Command ^
  "$ws = New-Object -ComObject WScript.Shell; ^
   $s = $ws.CreateShortcut('%USERPROFILE%\Desktop\My Browser.lnk'); ^
   $s.TargetPath = '%INSTALL_DIR%\run.bat'; ^
   $s.WorkingDirectory = '%INSTALL_DIR%'; ^
   $s.IconLocation = 'shell32.dll,14'; ^
   $s.Description = 'Privacy Browser with AI Chatbot and Security Tools'; ^
   $s.Save()"

echo [92m  Desktop shortcut created[0m
echo.

:: ============================================
:: DEPENDENCY CHECKS
:: ============================================

echo [93mChecking dependencies...[0m
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [91m  Python not found![0m
    echo [93m  Download from: https://www.python.org/downloads/[0m
    echo [93m  Make sure to check "Add Python to PATH" during install.[0m
    echo.
) else (
    for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo [92m  %%v found[0m
)

:: Check PyQt6
python -c "import PyQt6" 2>nul
if %errorlevel% neq 0 (
    echo [93m  PyQt6 not found. Installing...[0m
    pip install PyQt6 PyQt6-WebEngine
    if %errorlevel% equ 0 (
        echo [92m  PyQt6 installed[0m
    ) else (
        echo [91m  PyQt6 installation failed[0m
        echo [93m  Run manually: pip install PyQt6 PyQt6-WebEngine[0m
    )
) else (
    echo [92m  PyQt6 installed[0m
)

:: Check Flask
python -c "import flask, flask_cors, requests" 2>nul
if %errorlevel% neq 0 (
    echo [93m  Flask dependencies missing. Installing...[0m
    pip install flask flask-cors requests
    if %errorlevel% equ 0 (
        echo [92m  Flask dependencies installed[0m
    ) else (
        echo [93m  Could not install Flask - AI may not work[0m
    )
) else (
    echo [92m  Flask dependencies installed[0m
)

echo.

:: ============================================
:: OLLAMA CHECK
:: ============================================

echo [94mChecking for Ollama...[0m
where ollama >nul 2>&1
if %errorlevel% equ 0 (
    echo [92m  Ollama is installed[0m
    curl -s http://localhost:11434/api/tags >nul 2>&1
    if %errorlevel% equ 0 (
        echo [92m  Ollama is running[0m
    ) else (
        echo [93m  Ollama installed but not running[0m
        echo [94m  Start with: ollama serve[0m
    )
) else (
    echo [93m  Ollama not found[0m
    echo [94m  To enable AI chatbot:[0m
    echo [94m    1. Download: https://ollama.ai[0m
    echo [94m    2. Pull model: ollama pull mistral[0m
    echo [94m    3. Start: ollama serve[0m
    echo.
    echo [93m  (Browser works without Ollama, but AI chatbot will be limited)[0m
)

echo.

:: Create logs directory
if not exist "%USERPROFILE%\.mybrowser\logs" mkdir "%USERPROFILE%\.mybrowser\logs"

:: ============================================
:: INSTALLATION COMPLETE
:: ============================================

echo [92m==================================================[0m
echo [92m   INSTALLATION COMPLETE![0m
echo [92m==================================================[0m
echo.
echo [94mMy Browser - Complete Edition installed![0m
echo.
echo   Installation : %INSTALL_DIR%
echo   Logs         : %USERPROFILE%\.mybrowser\logs
echo.

echo [93mInstalled files:[0m
dir /B "%INSTALL_DIR%" 2>nul | findstr /v "^$"
echo.

if exist "%INSTALL_DIR%\modules\" (
    echo [92mMicroservices Status:[0m
    if exist "%INSTALL_DIR%\modules\network_interceptor.py" echo    Network Request Interceptor
    if exist "%INSTALL_DIR%\modules\ip_masking.py"          echo    IP Masking Monitor
    if exist "%INSTALL_DIR%\modules\social_tabs.py"         echo    Social Media Quick Tabs
    if exist "%INSTALL_DIR%\modules\security_monitor.py"    echo    Security Dashboard
    echo.
)

echo [93mHOW TO RUN:[0m
echo.
echo   Option 1: Double-click "My Browser" on Desktop
echo   Option 2: Run %INSTALL_DIR%\run.bat
echo   Option 3: python %INSTALL_DIR%\launch_mybrowser.py
echo.

echo [94mFEATURES:[0m
echo    All search engines
echo    Privacy logging ^& bookmarks
echo    Extensions ^& downloads
if exist "%INSTALL_DIR%\ollama_cors_proxy.py" echo    AI Chatbot (if Ollama running)
if exist "%INSTALL_DIR%\modules\" (
    echo    Social Media Quick Tabs
    echo    IP Masking Monitor
    echo    Network Request Interceptor
    echo    Security Dashboard
)

echo.
echo Enjoy your complete browser with AI ^& security tools!
echo.

set /p launch="Launch browser now? (y/n): "
if /i "%launch%"=="y" (
    echo.
    cd /d "%INSTALL_DIR%"
    call run.bat
)