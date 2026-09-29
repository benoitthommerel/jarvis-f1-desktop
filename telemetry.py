import socket
import struct
from threading import Event

from PyQt5.QtCore import QThread, pyqtSignal


class TelemetryListener(QThread):
    """Non-blocking F1 UDP listener.

    It validates the packet header and exposes safe, generic packet metadata.
    Game packet layouts can change by title/version, so detailed decoding is
    intentionally isolated for later version-specific adapters.
    """
    updated = pyqtSignal(dict)

    def __init__(self, host="0.0.0.0", port=20777):
        super().__init__()
        self.host, self.port = host, port
        self.stop_event = Event()
        self.latest = {"connected": False, "packet_id": None, "packets": 0, "address": host}
        self.sock = None

    def snapshot(self):
        return dict(self.latest)

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(0.25)
        try:
            self.sock.bind((self.host, self.port))
            while not self.stop_event.is_set():
                try:
                    payload, address = self.sock.recvfrom(4096)
                except socket.timeout:
                    continue
                packet_id = payload[5] if len(payload) > 5 else None
                self.latest.update({"connected": True, "packet_id": packet_id, "packets": self.latest["packets"] + 1, "address": address[0]})
                self.updated.emit(self.snapshot())
        except OSError as error:
            self.latest.update({"connected": False, "error": str(error)})
            self.updated.emit(self.snapshot())
        finally:
            if self.sock:
                self.sock.close()

    def stop(self):
        self.stop_event.set()
