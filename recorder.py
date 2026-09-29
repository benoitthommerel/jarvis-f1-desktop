"""Session recording and analysis."""
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from decoders import CarTelemetry, LapData, SessionData


class SessionRecorder:
    """Record telemetry and session data to disk in real time."""

    def __init__(self, output_dir: Path | str = "sessions"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_name = f"session_{timestamp}"
        self.session_dir = self.output_dir / self.session_name
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.telemetry_file = self.session_dir / "telemetry.csv"
        self.lap_data_file = self.session_dir / "laps.csv"
        self.session_file = self.session_dir / "session.json"
        self.telemetry_writer = None
        self.lap_writer = None
        self.session_meta = {"start": datetime.now().isoformat(), "packets": 0}

    def start(self):
        """Start recording telemetry."""
        if self.telemetry_file.exists():
            self.telemetry_file.unlink()
        if self.lap_data_file.exists():
            self.lap_data_file.unlink()
        self.telemetry_file.touch()
        self.lap_data_file.touch()

    def record_telemetry(self, frame_id: int, car_index: int, telemetry: CarTelemetry):
        """Append car telemetry to CSV."""
        try:
            with open(self.telemetry_file, "a", newline="") as f:
                if f.tell() == 0:
                    writer = csv.DictWriter(
                        f,
                        fieldnames=[
                            "frame",
                            "car",
                            "speed",
                            "rpm",
                            "gear",
                            "throttle",
                            "brake",
                            "drs",
                            "ers_pct",
                            "engine_temp",
                            "tire_fl",
                            "tire_fr",
                            "tire_rl",
                            "tire_rr",
                        ],
                    )
                    writer.writeheader()
                else:
                    writer = csv.DictWriter(f, fieldnames=[
                            "frame",
                            "car",
                            "speed",
                            "rpm",
                            "gear",
                            "throttle",
                            "brake",
                            "drs",
                            "ers_pct",
                            "engine_temp",
                            "tire_fl",
                            "tire_fr",
                            "tire_rl",
                            "tire_rr",
                        ])
                writer.writerow(
                    {
                        "frame": frame_id,
                        "car": car_index,
                        "speed": telemetry.speed,
                        "rpm": telemetry.rpm,
                        "gear": telemetry.gear,
                        "throttle": telemetry.throttle,
                        "brake": telemetry.brake,
                        "drs": 1 if telemetry.drs else 0,
                        "ers_pct": round(telemetry.ers_battery_percent * 100, 1),
                        "engine_temp": telemetry.engine_temp,
                        "tire_fl": telemetry.tire_temp_front_left,
                        "tire_fr": telemetry.tire_temp_front_right,
                        "tire_rl": telemetry.tire_temp_rear_left,
                        "tire_rr": telemetry.tire_temp_rear_right,
                    }
                )
                self.session_meta["packets"] += 1
        except (IOError, OSError) as e:
            print(f"Record telemetry error: {e}")

    def record_lap(self, car_index: int, lap_data: LapData):
        """Append lap data to CSV."""
        try:
            with open(self.lap_data_file, "a", newline="") as f:
                if f.tell() == 0:
                    writer = csv.DictWriter(
                        f,
                        fieldnames=[
                            "car",
                            "lap",
                            "pos",
                            "lap_time",
                            "s1",
                            "s2",
                            "distance",
                            "wear_fl",
                            "wear_fr",
                            "wear_rl",
                            "wear_rr",
                        ],
                    )
                    writer.writeheader()
                else:
                    writer = csv.DictWriter(f, fieldnames=[
                            "car",
                            "lap",
                            "pos",
                            "lap_time",
                            "s1",
                            "s2",
                            "distance",
                            "wear_fl",
                            "wear_fr",
                            "wear_rl",
                            "wear_rr",
                        ])
                writer.writerow(
                    {
                        "car": car_index,
                        "lap": lap_data.current_lap_num,
                        "pos": lap_data.car_position,
                        "lap_time": round(lap_data.last_lap_time, 3),
                        "s1": round(lap_data.sector1_time, 3),
                        "s2": round(lap_data.sector2_time, 3),
                        "distance": round(lap_data.total_distance, 1),
                        "wear_fl": lap_data.tire_wear_front_left,
                        "wear_fr": lap_data.tire_wear_front_right,
                        "wear_rl": lap_data.tire_wear_rear_left,
                        "wear_rr": lap_data.tire_wear_rear_right,
                    }
                )
        except (IOError, OSError) as e:
            print(f"Record lap error: {e}")

    def record_session(self, session_data: SessionData):
        """Save session metadata to JSON."""
        try:
            meta = {
                **self.session_meta,
                "weather": session_data.weather,
                "track_temp": session_data.track_temp,
                "air_temp": session_data.air_temp,
                "track_length": session_data.track_length,
                "session_type": session_data.session_type,
                "total_laps": session_data.session_total_laps,
                "safety_car": session_data.safety_car_status,
            }
            self.session_file.write_text(json.dumps(meta, indent=2))
        except (IOError, OSError) as e:
            print(f"Record session error: {e}")

    def finalize(self):
        """Finalize session recording."""
        self.session_meta["end"] = datetime.now().isoformat()
        self.record_session(SessionData(
            weather="",
            track_temp=0,
            air_temp=0,
            track_length=0,
            session_type="",
            session_time_left=0,
            session_total_laps=0,
            session_lap=0,
            safety_car_status="",
        ))
