import sys
import json
import os
from pathlib import Path

try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                  QHBoxLayout, QPushButton, QComboBox, QLineEdit, 
                                  QLabel, QTextEdit, QDialog, QMessageBox)
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5.QtCore import QUrl, Qt, QSettings
    from PyQt5.QtGui import QIcon, QFont
except ImportError:
    print("PyQt5 not installed. Installing...")
    os.system("pip install PyQt5 PyQtWebEngine")
    from PyQt5.QtWidgets import *
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5.QtCore import QUrl, Qt, QSettings
    from PyQt5.QtGui import QIcon, QFont

# ============ HTML CONTENT ============
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>JARVIS F1 Dashboard</title>
  <style>
    :root {
      --bg: #020b14;
      --cyan: #00eaff;
      --green: #57ffb8;
      --amber: #ffb454;
      --red: #ff4d6d;
      --white: #edfaff;
      --muted: #9ac4d7;
    }

    * { box-sizing: border-box; }
    html, body {
      margin: 0; height: 100%;
      background: radial-gradient(circle at center, #061421 0%, #020b14 45%, #01060d 100%);
      color: var(--white);
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      overflow: hidden;
    }

    body { display: flex; align-items: center; justify-content: center; }

    .hud {
      width: 100vw;
      height: 100vh;
      padding: 18px;
      background: linear-gradient(180deg, rgba(5,20,28,0.96), rgba(2,10,18,0.98));
      border: 1px solid rgba(0,234,255,0.35);
      box-shadow: inset 0 0 40px rgba(0,234,255,0.1), 0 0 30px rgba(0,234,255,0.08);
      display: grid;
      grid-template-columns: 320px 1fr 300px;
      grid-template-rows: 60px 1fr 140px;
      gap: 12px;
    }

    .panel {
      position: relative;
      background: rgba(9, 21, 31, 0.78);
      border: 1px solid rgba(0,234,255,0.35);
      box-shadow: 0 0 12px rgba(0,234,255,0.08);
      overflow: hidden;
      padding: 12px 14px;
    }

    .header {
      grid-column: 1 / 4;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 14px;
    }

    .brand {
      font-size: 14px;
      letter-spacing: 2px;
      color: var(--cyan);
      text-transform: uppercase;
    }

    .brand strong {
      color: white;
      letter-spacing: 4px;
      font-weight: 700;
    }

    .status-box {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 11px;
      letter-spacing: 1px;
    }

    .dot {
      width: 10px; height: 10px; border-radius: 50%;
      background: var(--green);
      box-shadow: 0 0 12px var(--green);
      animation: pulse 1.4s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: .5; }
    }

    .left-stack, .right-stack {
      display: flex;
      flex-direction: column;
      gap: 12px;
      min-height: 0;
    }

    .card {
      position: relative;
      min-height: 120px;
    }

    .card-title {
      font-size: 10px;
      letter-spacing: 2px;
      color: var(--cyan);
      text-transform: uppercase;
      margin-bottom: 10px;
    }

    .position-line {
      display: flex;
      justify-content: space-between;
      align-items: end;
      margin-top: 12px;
    }

    .position {
      font-size: 30px;
      font-weight: 800;
      color: var(--green);
    }

    .lap {
      font-size: 18px;
      color: var(--white);
      font-weight: 700;
    }

    .monitor {
      min-height: 170px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(8, 18, 25, 0.5);
      border: 1px dashed rgba(0,234,255,0.35);
    }

    .center-panel {
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(8, 18, 25, 0.75);
      border: 1px solid rgba(0,234,255,0.35);
      overflow: hidden;
    }

    .engine-core {
      position: relative;
      width: 400px;
      height: 400px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .ring {
      position: absolute;
      border-radius: 50%;
      border: 1px solid rgba(0,234,255,0.8);
      box-shadow: 0 0 12px rgba(0,234,255,0.4);
    }

    .ring.one {
      width: 380px; height: 380px;
      border-style: dashed;
      animation: spin 18s linear infinite reverse;
    }

    .ring.two {
      width: 300px; height: 300px;
      border-width: 2px;
      animation: spin 12s linear infinite;
    }

    .ring.three {
      width: 210px; height: 210px;
      border-style: dotted;
      animation: spin 9s linear infinite reverse;
    }

    .core {
      width: 100px; height: 100px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(0,234,255,1), rgba(0,234,255,0.5));
      box-shadow: 0 0 30px rgba(0,234,255,0.75);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #04151e;
      font-weight: 900;
      font-size: 16px;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    .tire-box {
      position: absolute;
      background: rgba(8, 18, 25, 0.9);
      border: 1px solid rgba(0,234,255,0.35);
      padding: 8px 10px;
      font-size: 10px;
    }

    .tire-box.fl { left: 18px; top: 28px; }
    .tire-box.fr { right: 18px; top: 28px; }
    .tire-box.rl { left: 18px; bottom: 26px; }
    .tire-box.rr { right: 18px; bottom: 26px; }

    .tire-box .label { color: var(--cyan); }
    .tire-box .temp { color: var(--amber); font-weight: 700; }
    .tire-box .press { color: var(--green); font-weight: 700; }

    .right-stack .card { flex: 1; }

    .bio-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 10px;
      margin-bottom: 10px;
    }

    .value {
      font-size: 20px;
      font-weight: 800;
      margin-top: 6px;
    }

    .mini-chart {
      width: 100%;
      height: 36px;
      margin-top: 8px;
    }

    .footer {
      grid-column: 1 / 4;
      display: grid;
      grid-template-columns: 2fr 1fr 1fr;
      gap: 12px;
    }

    .meter {
      height: 12px;
      background: rgba(0,234,255,0.07);
      border: 1px solid rgba(0,234,255,0.35);
      margin-top: 8px;
    }

    .meter span {
      display: block;
      height: 100%;
      width: 78%;
      background: linear-gradient(90deg, var(--cyan), var(--amber), var(--red));
      box-shadow: 0 0 12px rgba(0,234,255,0.45);
    }

    .metric {
      font-size: 22px;
      font-weight: 800;
    }

    .metric.green { color: var(--green); }
    .metric.orange { color: var(--amber); }
    .metric.cyan { color: var(--cyan); }
  </style>
</head>
<body>
  <div class="hud">
    <div class="header panel">
      <div class="brand"><strong>JARVIS</strong> // race engineer</div>
      <div class="status-box">
        <span class="dot"></span>
        <span id="status-text">Online / local</span>
      </div>
    </div>

    <div class="left-stack">
      <div class="panel card">
        <div class="card-title">Race status</div>
        <div class="position-line">
          <div>
            <div style="font-size:10px; color:#9ac4d7;">Position</div>
            <div class="position">P1</div>
          </div>
          <div style="text-align:right;">
            <div style="font-size:10px; color:#9ac4d7;">Lap</div>
            <div class="lap">16 / 67</div>
          </div>
        </div>
      </div>

      <div class="panel card monitor">
        TRACK VISUALIZATION
      </div>
    </div>

    <div class="panel center-panel">
      <div class="engine-core">
        <div class="ring one"></div>
        <div class="ring two"></div>
        <div class="ring three"></div>
        <div class="core">JARVIS</div>

        <div class="tire-box fl">
          <div class="label">FL</div>
          <div><span class="temp">104°C</span> | <span class="press">1.2B</span></div>
        </div>
        <div class="tire-box fr">
          <div class="label">FR</div>
          <div><span class="temp">105°C</span> | <span class="press">1.1B</span></div>
        </div>
        <div class="tire-box rl">
          <div class="label">RL</div>
          <div><span class="temp">113°C</span> | <span class="press">1.2B</span></div>
        </div>
        <div class="tire-box rr">
          <div class="label">RR</div>
          <div><span class="temp">115°C</span> | <span class="press">1.3B</span></div>
        </div>
      </div>
    </div>

    <div class="right-stack">
      <div class="panel card">
        <div class="bio-header">
          <span>Heart rate</span>
          <span style="color:var(--green);">65 BPM</span>
        </div>
        <svg class="mini-chart" viewBox="0 0 200 40" preserveAspectRatio="none">
          <path style="stroke:var(--green); fill:none; stroke-width:2;" d="M 0 23 Q 30 10 60 20 T 120 18 T 170 10 T 200 15"></path>
        </svg>
      </div>

      <div class="panel card">
        <div class="bio-header">
          <span>Breath</span>
          <span style="color:var(--cyan);">12</span>
        </div>
        <svg class="mini-chart" viewBox="0 0 200 40" preserveAspectRatio="none">
          <path style="stroke:var(--cyan); fill:none; stroke-width:2;" d="M 0 25 Q 45 5 90 20 T 170 22 T 200 18"></path>
        </svg>
      </div>

      <div class="panel card">
        <div class="bio-header">
          <span>Stress</span>
          <span style="color:var(--amber);">51/100</span>
        </div>
        <svg class="mini-chart" viewBox="0 0 200 40" preserveAspectRatio="none">
          <path style="stroke:var(--amber); fill:none; stroke-width:2;" d="M 0 24 L 30 18 L 65 23 L 90 15 L 130 20 L 170 14 L 200 8"></path>
        </svg>
      </div>
    </div>

    <div class="footer">
      <div class="panel card">
        <div class="card-title">RPM moteur</div>
        <div style="font-size:10px; color:#9ac4d7;">11,850</div>
        <div class="meter"><span></span></div>
      </div>

      <div class="panel card">
        <div class="card-title">Engine temp</div>
        <div class="metric orange">112°C</div>
      </div>

      <div class="panel card">
        <div class="card-title">Fuel</div>
        <div class="metric green">48.2%</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

# ============ MAIN APPLICATION ============
class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("JARVIS AI Config")
        self.setGeometry(100, 100, 500, 350)
        self.setStyleSheet("""
            QDialog { background-color: #020b14; color: #edfaff; }
            QLabel { color: #00eaff; font-weight: bold; }
            QLineEdit, QComboBox, QTextEdit { 
                background-color: #0c1d2b; 
                color: #edfaff;
                border: 1px solid #00eaff;
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton {
                background-color: #00eaff;
                color: #020b14;
                font-weight: bold;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover { background-color: #57ffb8; }
        """)
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("AI Provider:"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["OpenAI", "Anthropic Claude", "Google Gemini", "Groq", "Local Ollama"])
        layout.addWidget(self.provider_combo)
        
        layout.addWidget(QLabel("API Key:"))
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setPlaceholderText("sk-...")
        layout.addWidget(self.api_key_input)
        
        layout.addWidget(QLabel("Additional Keys (comma separated):"))
        self.extra_keys = QTextEdit()
        self.extra_keys.setPlaceholderText("sk-key1, sk-key2, sk-key3")
        layout.addWidget(self.extra_keys)
        
        layout.addWidget(QLabel("Routing Mode:"))
        self.routing_combo = QComboBox()
        self.routing_combo.addItems(["Auto Failover", "Manual Select", "Round Robin"])
        layout.addWidget(self.routing_combo)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save & Connect")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def get_config(self):
        return {
            "provider": self.provider_combo.currentText(),
            "api_key": self.api_key_input.text(),
            "extra_keys": [k.strip() for k in self.extra_keys.toPlainText().split(",") if k.strip()],
            "routing": self.routing_combo.currentText()
        }


class JarvisF1Desktop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS F1 Race Engineer Desktop")
        self.setGeometry(100, 100, 1400, 900)
        
        # Stylesheet
        self.setStyleSheet("""
            QMainWindow { background-color: #020b14; }
            QToolBar { background-color: #071621; border: 1px solid #00eaff; }
            QPushButton {
                background-color: #00eaff;
                color: #020b14;
                font-weight: bold;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover { background-color: #57ffb8; }
        """)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        mode_label = QLabel("Mode:")
        mode_label.setStyleSheet("color: #00eaff; font-weight: bold;")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Normal Dev", "F1 Engineer", "Discrete", "Background Worker"])
        self.mode_combo.setStyleSheet("""
            QComboBox { background-color: #0c1d2b; color: #edfaff; border: 1px solid #00eaff; padding: 6px; }
        """)
        
        config_btn = QPushButton("⚙ AI Config")
        config_btn.clicked.connect(self.open_config)
        
        toolbar_layout.addWidget(mode_label)
        toolbar_layout.addWidget(self.mode_combo)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(config_btn)
        
        layout.addLayout(toolbar_layout)
        
        # Web view
        self.browser = QWebEngineView()
        self.browser.setHtml(HTML_CONTENT)
        layout.addWidget(self.browser)
        
        self.load_config()
    
    def open_config(self):
        dialog = ConfigDialog(self)
        if dialog.exec_():
            config = dialog.get_config()
            self.save_config(config)
            QMessageBox.information(self, "Success", f"Configuration saved!\nProvider: {config['provider']}\nRouting: {config['routing']}")
    
    def save_config(self, config):
        settings = QSettings("Stark", "JARVIS")
        settings.setValue("provider", config["provider"])
        settings.setValue("api_key", config["api_key"])
        settings.setValue("extra_keys", json.dumps(config["extra_keys"]))
        settings.setValue("routing", config["routing"])
    
    def load_config(self):
        settings = QSettings("Stark", "JARVIS")
        provider = settings.value("provider", "OpenAI")


def main():
    app = QApplication(sys.argv)
    window = JarvisF1Desktop()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()