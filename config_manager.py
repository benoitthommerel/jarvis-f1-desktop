import json
import os
from pathlib import Path


class ConfigManager:
    """Small local configuration store; API keys never enter the dashboard HTML."""
    def __init__(self):
        self.path = Path.home() / ".jarvis-f1" / "config.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self):
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return {"provider": "local", "api_key": "", "backup_keys": [], "routing": "automatic", "mode": "Normal / Dev"}

    def save(self):
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")
        try:
            os.chmod(self.path, 0o600)
        except OSError:
            pass

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def update(self, values):
        self.data.update(values)
        self.save()
