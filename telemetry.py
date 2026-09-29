"""F1 25 UDP listener and safe packet-header decoder."""
from __future__ import annotations

import socket
import struct
import time
from threading import Event, Lock

from PyQt5.QtCore import QThread, pyqtSignal


PACKET_NAMES = {
    0: "Motion", 1: "Session", 2: "Lap Data", 3: "Event",
    4: "Participants", 5: "Car Setups", 6: "Car Telemetry",
    7: "Car Status", 8: "Final Classification", 9: "Lobby Info",
    10: "Car Damage", 11: "Session History", 12: "Tyre Sets",
    13: "Motion Ex",
}


class TelemetryListener(QThread):
    """Listen on UDP 20777 and decode the common 29-byte F1 25 header.

    The listener deliberately does not guess payload fields. Payload layouts
    are version-specific; adapters can be added without changing the UI.
    """
    updated = pyqtSignal(dict)

    def __init__(self, host="0.0.0.0", port=20777):
        super().__init__()
        self.host, self.port = host, port
        self.stop_event = Event()
        self.lock = Lock()
        self.sock = None
        self.latest = {
            "connected": False,
            "bound": False,
            "packet_id": None,
            "packet_name": "Unknown",
            "packets": 0,
            "bytes": 0,
            "address": None,
            "error": None,
            "last_packet_age": None,
        }

    @staticmethod
    def decode_header(payload: bytes) -> dict:
        if len(payload) < 29:
            raise ValueError(f"packet too short: {len(payload)} bytes")
        # F1 25 header: H, 5 bytes, Q, f, I, 3 bytes = 29 bytes, little endian.
        values = struct.unpack_from("<HBBBBBQfIBBB", payload)
        packet_format, game_year, major, minor, packet_version, packet_id = values[:6]
        return {
            "packet_format": packet_format,
            "game_year": game_year,
            "game_major": major,
            "game_minor": minor,
            "packet_version": packet_version,
            "packet_id": packet_id,
            "packet_name": PACKET_NAMES.get(packet_id, "Unknown"),
            "session_uid": values[6],
            "session_time": values[7],
            "frame_identifier": values[8],
            "overall_frame_identifier": values[9],
            "player_car_index": values[10],
            "secondary_player_car_index": values[11],
            "payload_size": len(payload) - 29,
        }

    def snapshot(self):
        with self.lock:
            result = dict(self.latest)
        if result["last_packet_age"] is not None:
            result["last_packet_age"] = round(time.monotonic() - result["last_packet_age"], 2)
        return result

    def _update(self, values):
        with self.lock:
            self.latest.update(values)
        self.updated.emit(self.snapshot())

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(0.25)
        try:
            self.sock.bind((self.host, self.port))
            self._update({"bound": True, "error": None})
            while not self.stop_event.is_set():
                try:
                    payload, address = self.sock.recvfrom(8192)
                except socket.timeout:
                    continue
                try:
                    header = self.decode_header(payload)
                except ValueError as error:
                    self._update({"error": str(error), "address": address[0]})
                    continue
                self._update({
                    **header,
                    "connected": True,
                    "address": address[0],
                    "packets": self.latest["packets"] + 1,
                    "bytes": self.latest["bytes"] + len(payload),
                    "last_packet_age": time.monotonic(),
                    "error": None,
                })
        except OSError as error:
            self._update({"error": str(error), "bound": False})
        finally:
            if self.sock is not None:
                self.sock.close()
                self.sock = None

    def stop(self):
        self.stop_event.set()
        if self.sock is not None:
            try:
                self.sock.close()
            except OSError:
                pass
