#!/bin/bash

echo "======================================="
echo "  JARVIS F1 RACE ENGINEER - Desktop"
echo "======================================="

if ! command -v python3 &> /dev/null; then
    echo "[-] Python3 non detecte. Installation..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install python3
    else
        sudo apt update && sudo apt install -y python3 python3-pip
    fi
fi

echo "[+] Installation des dependances..."
pip3 install PyQt5 PyQtWebEngine

echo "[+] Lancement de JARVIS F1 Desktop..."
python3 app.py