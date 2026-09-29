from __future__ import annotations

import json
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton,
    QVBoxLayout, QWidget,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView

from config_manager import ConfigManager
from dashboards import DASHBOARDS
from telemetry import TelemetryListener


class ApiDialog(QDialog):
    def __init__(self, config: ConfigManager, parent=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("JARVIS — AI configuration")
        self.setMinimumWidth(520)
        form = QFormLayout(self)
        self.provider = QComboBox()
        self.provider.addItems(["local", "openai", "anthropic", "gemini", "groq"])
        self.provider.setCurrentText(config.get("provider", "local"))
        self.key = QLineEdit(config.get("api_key", ""))
        self.key.setEchoMode(QLineEdit.Password)
        self.key.setPlaceholderText("Leave empty for local mode")
        self.backups = QLineEdit(", ".join(config.get("backup_keys", [])))
        self.backups.setEchoMode(QLineEdit.Password)
        self.routing = QComboBox()
        self.routing.addItems(["automatic", "manual", "round_robin"])
        self.routing.setCurrentText(config.get("routing", "automatic"))
        form.addRow("Provider", self.provider)
        form.addRow("Primary API key", self.key)
        form.addRow("Backup keys", self.backups)
        form.addRow("Routing", self.routing)
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def save(self):
        self.config.update({
            "provider": self.provider.currentText(),
            "api_key": self.key.text().strip(),
            "backup_keys": [x.strip() for x in self.backups.text().split(",") if x.strip()],
            "routing": self.routing.currentText(),
        })
        self.accept()


class JarvisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = ConfigManager()
        self.telemetry = TelemetryListener()
        self.telemetry.updated.connect(self.on_telemetry)
        self.telemetry.start()
        self.setWindowTitle("JARVIS F1 Desktop")
        self.resize(1440, 900)
        self.setStyleSheet("""
            QMainWindow, QWidget { background: #020b14; color: #edfaff; }
            QComboBox, QPushButton { background: #0c1d2b; color: #edfaff; border: 1px solid #00eaff; padding: 7px 10px; }
            QPushButton:hover, QComboBox:hover { background: #12354a; }
            QLabel { color: #00eaff; }
        """)
        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        bar = QHBoxLayout()
        bar.addWidget(QLabel("MODE"))
        self.mode = QComboBox()
        self.mode.addItems(list(DASHBOARDS.keys()))
        self.mode.setCurrentText(self.config.get("mode", "Normal / Dev"))
        self.mode.currentTextChanged.connect(self.change_mode)
        bar.addWidget(self.mode)
        self.connection = QLabel("UDP: starting listener")
        bar.addWidget(self.connection)
        bar.addStretch()
        config_button = QPushButton("⚙ AI CONFIG")
        config_button.clicked.connect(self.open_config)
        bar.addWidget(config_button)
        layout.addLayout(bar)
        self.view = QWebEngineView()
        layout.addWidget(self.view)
        self.change_mode(self.mode.currentText())
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_dashboard)
        self.timer.start(500)

    def change_mode(self, mode: str):
        self.config.set("mode", mode)
        self.view.setHtml(DASHBOARDS[mode])

    def refresh_dashboard(self):
        data = self.telemetry.snapshot()
        self.view.page().runJavaScript(
            "window.jarvisUpdate && window.jarvisUpdate(%s);" % json.dumps(data)
        )
        if data.get("error") and not data.get("bound"):
            self.connection.setText("UDP ERROR: %s" % data["error"])
        elif data.get("connected"):
            self.connection.setText(
                "UDP LIVE: %s · %s packets" % (data.get("packet_name", "packet"), data["packets"])
            )
        elif data.get("bound"):
            self.connection.setText("UDP: listening on 20777")

    def on_telemetry(self, data: dict):
        self.refresh_dashboard()

    def open_config(self):
        if ApiDialog(self.config, self).exec_():
            provider = self.config.get("provider", "local")
            QMessageBox.information(self, "JARVIS", "Configuration saved for %s." % provider)

    def closeEvent(self, event):
        self.telemetry.stop()
        self.telemetry.wait(1000)
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("JARVIS F1")
    window = JarvisWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
