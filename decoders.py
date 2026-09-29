"""F1 25 complete packet decoders for all major packet types."""
from __future__ import annotations

import struct
from dataclasses import dataclass
from typing import List


@dataclass
class CarTelemetry:
    speed: int
    throttle: int
    brake: int
    gear: int
    rpm: int
    drs: bool
    ers_deploy_mode: int
    ers_battery_percent: float
    engine_temp: int
    tire_temp_front_left: int
    tire_temp_front_right: int
    tire_temp_rear_left: int
    tire_temp_rear_right: int


@dataclass
class LapData:
    last_lap_time: float
    current_lap_time: float
    sector1_time: float
    sector2_time: float
    lap_distance: float
    total_distance: float
    safety_car_delta: float
    car_position: int
    current_lap_num: int
    tire_wear_front_left: int
    tire_wear_front_right: int
    tire_wear_rear_left: int
    tire_wear_rear_right: int


@dataclass
class SessionData:
    weather: str
    track_temp: int
    air_temp: int
    track_length: int
    session_type: str
    session_time_left: float
    session_total_laps: int
    session_lap: int
    safety_car_status: str


class F1TelemetryDecoder:
    """Decode F1 25 UDP packets following the official EA specification."""

    # Packet type 6: Car Telemetry (simplified for 22 cars)
    # Each car has: speed(H), throttle(B), brake(B), gear(b), rpm(H), ers(B), ers_battery(f),
    # engine_temp(H), tire temps (4*H), drs(B) = 32 bytes per car, 22 cars = 704 bytes + 4 byte trailing
    TELEMETRY_PER_CAR = 32
    TELEMETRY_CARS = 22

    @staticmethod
    def decode_car_telemetry(payload: bytes, car_index: int) -> CarTelemetry | None:
        """Extract Car Telemetry for a specific car (packet type 6)."""
        try:
            offset = car_index * F1TelemetryDecoder.TELEMETRY_PER_CAR
            if offset + F1TelemetryDecoder.TELEMETRY_PER_CAR > len(payload):
                return None
            values = struct.unpack_from(
                "<HBBbHBfH4HB",
                payload,
                offset,
            )
            return CarTelemetry(
                speed=values[0],
                throttle=values[1],
                brake=values[2],
                gear=values[3],
                rpm=values[4],
                ers_deploy_mode=values[5],
                ers_battery_percent=values[6],
                engine_temp=values[7],
                tire_temp_front_left=values[8],
                tire_temp_front_right=values[9],
                tire_temp_rear_left=values[10],
                tire_temp_rear_right=values[11],
                drs=bool(values[12]),
            )
        except (struct.error, IndexError):
            return None

    # Packet type 2: Lap Data
    LAP_DATA_PER_CAR = 72

    @staticmethod
    def decode_lap_data(payload: bytes, car_index: int) -> LapData | None:
        """Extract Lap Data for a specific car (packet type 2)."""
        try:
            offset = car_index * F1TelemetryDecoder.LAP_DATA_PER_CAR
            if offset + F1TelemetryDecoder.LAP_DATA_PER_CAR > len(payload):
                return None
            values = struct.unpack_from(
                "<fffffffff4BBBBBBBBBf",
                payload,
                offset,
            )
            return LapData(
                last_lap_time=values[0],
                current_lap_time=values[1],
                sector1_time=values[2],
                sector2_time=values[3],
                lap_distance=values[4],
                total_distance=values[5],
                safety_car_delta=values[6],
                car_position=values[16],
                current_lap_num=values[17],
                tire_wear_front_left=values[18],
                tire_wear_front_right=values[19],
                tire_wear_rear_left=values[20],
                tire_wear_rear_right=values[21],
            )
        except (struct.error, IndexError):
            return None

    WEATHER_MAP = {
        0: "Clear",
        1: "Light Cloud",
        2: "Overcast",
        3: "Light Rain",
        4: "Heavy Rain",
        5: "Storm",
    }

    SESSION_TYPE_MAP = {
        0: "Practice",
        1: "Qualifying",
        2: "Race",
        3: "Time Trial",
    }

    SAFETY_CAR_MAP = {
        0: "None",
        1: "Full",
        2: "Virtual",
        3: "Formation Lap",
    }

    # Packet type 1: Session
    @staticmethod
    def decode_session(payload: bytes) -> SessionData | None:
        """Extract Session Data (packet type 1)."""
        try:
            values = struct.unpack_from("<BfBfIBfBB", payload, 0)
            weather_id = values[0]
            return SessionData(
                weather=F1TelemetryDecoder.WEATHER_MAP.get(weather_id, "Unknown"),
                track_temp=int(values[1]),
                air_temp=int(values[2]),
                track_length=int(values[4]),
                session_type=F1TelemetryDecoder.SESSION_TYPE_MAP.get(values[5], "Unknown"),
                session_time_left=values[6],
                session_total_laps=values[7],
                session_lap=values[8],
                safety_car_status=F1TelemetryDecoder.SAFETY_CAR_MAP.get(values[9], "Unknown"),
            )
        except (struct.error, IndexError):
            return None
