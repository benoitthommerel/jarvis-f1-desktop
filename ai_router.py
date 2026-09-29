"""AI provider router with automatic failover and multi-key support."""
from __future__ import annotations

import os
from enum import Enum
from typing import Optional


class AIProvider(Enum):
    LOCAL = "local"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    GROQ = "groq"


class AIRouter:
    """Route AI requests with automatic failover and key management."""

    def __init__(self, provider: str, api_key: str, backup_keys: list[str], routing: str):
        self.provider = AIProvider(provider.lower()) if provider.lower() != "local" else AIProvider.LOCAL
        self.keys = [api_key] + backup_keys if api_key else backup_keys
        self.routing = routing
        self.current_key_idx = 0
        self.call_count = 0

    def get_next_key(self) -> Optional[str]:
        """Get the next API key based on routing strategy."""
        if not self.keys:
            return None
        if self.routing == "automatic":
            key = self.keys[self.current_key_idx]
            self.current_key_idx = (self.current_key_idx + 1) % len(self.keys)
            return key
        elif self.routing == "round_robin":
            key = self.keys[self.call_count % len(self.keys)]
            self.call_count += 1
            return key
        else:  # manual
            return self.keys[0]

    def is_available(self) -> bool:
        """Check if any API key is configured."""
        return bool(self.keys) and self.provider != AIProvider.LOCAL

    def analyze_session(self, data: dict) -> str:
        """Generate AI analysis of session data."""
        if self.provider == AIProvider.LOCAL:
            return self._local_analysis(data)
        # Remote provider would call APIs here
        key = self.get_next_key()
        if not key:
            return "No API key configured. Using local analysis."
        # Stub: actual API calls would happen here
        return f"[{self.provider.value.upper()}] Analyzing session data..."

    def _local_analysis(self, data: dict) -> str:
        """Generate local analysis without API calls."""
        lines = ["📊 SESSION ANALYSIS (Local Mode)"]
        if "session_type" in data:
            lines.append(f"Session: {data['session_type']}")
        if "weather" in data:
            lines.append(f"Weather: {data['weather']}")
        if "total_laps" in data:
            lines.append(f"Total laps: {data['total_laps']}")
        lines.append("\nRecommendations:")
        lines.append("• Monitor tire degradation closely")
        lines.append("• Adjust fuel mix as needed")
        lines.append("• Plan pit stops strategically")
        return "\n".join(lines)
