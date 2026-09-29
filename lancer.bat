@echo off
title JARVIS F1 Desktop - Launcher
color 0B

echo ===============================================
echo   JARVIS F1 RACE ENGINEER - Desktop Edition
echo ===============================================

:: Verifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [-] Python non detecte. Installation...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe' -OutFile '%TEMP%\python.exe' ; Start-Process '%TEMP%\python.exe' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait"
)

echo [+] Installation des dependances...
pip install PyQt5 PyQtWebEngine --quiet

echo [+] Lancement de JARVIS F1 Desktop...
python app.py

pause