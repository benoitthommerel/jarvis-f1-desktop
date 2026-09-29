"""Real-time telemetry analysis and performance metrics."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional

from decoders import CarTelemetry, LapData


@dataclass
class PerformanceMetrics:
    avg_speed: float
    max_rpm: int
    avg_throttle: float
    avg_brake: float
    engine_temp_max: int
    tire_degradation: Dict[str, float]
    sector_times: Dict[str, float]
    delta_to_leader: float


class TelemetryAnalyzer:
    """Real-time analysis of F1 telemetry data."""

    def __init__(self, max_samples: int = 500):
        self.max_samples = max_samples
        self.car_history: Dict[int, deque] = {}
        self.lap_times: Dict[int, List[float]] = {}
        self.best_lap: Dict[int, float] = {}
        self.positions: Dict[int, int] = {}

    def update(self, car_index: int, telemetry: CarTelemetry):
        """Update telemetry history for a car."""
        if car_index not in self.car_history:
            self.car_history[car_index] = deque(maxlen=self.max_samples)
        self.car_history[car_index].append(telemetry)

    def update_lap(self, car_index: int, lap_data: LapData):
        """Record lap data and update position."""
        if car_index not in self.lap_times:
            self.lap_times[car_index] = []
            self.best_lap[car_index] = float("inf")
        if lap_data.last_lap_time > 0:
            self.lap_times[car_index].append(lap_data.last_lap_time)
            self.best_lap[car_index] = min(self.best_lap[car_index], lap_data.last_lap_time)
        self.positions[car_index] = lap_data.car_position

    def get_metrics(self, car_index: int) -> Optional[PerformanceMetrics]:
        """Calculate performance metrics for a car."""
        if car_index not in self.car_history or not self.car_history[car_index]:
            return None
        history = list(self.car_history[car_index])
        avg_speed = sum(t.speed for t in history) / len(history)
        max_rpm = max(t.rpm for t in history)
        avg_throttle = sum(t.throttle for t in history) / len(history)
        avg_brake = sum(t.brake for t in history) / len(history)
        engine_temp_max = max(t.engine_temp for t in history)
        return PerformanceMetrics(
            avg_speed=round(avg_speed, 1),
            max_rpm=max_rpm,
            avg_throttle=round(avg_throttle, 1),
            avg_brake=round(avg_brake, 1),
            engine_temp_max=engine_temp_max,
            tire_degradation={
                "FL": 100 - (sum(t.tire_temp_front_left for t in history) / len(history) / 1.2),
                "FR": 100 - (sum(t.tire_temp_front_right for t in history) / len(history) / 1.2),
                "RL": 100 - (sum(t.tire_temp_rear_left for t in history) / len(history) / 1.2),
                "RR": 100 - (sum(t.tire_temp_rear_right for t in history) / len(history) / 1.2),
            },
            sector_times={
                "best": self.best_lap.get(car_index, 0),
                "recent": self.lap_times[car_index][-1] if car_index in self.lap_times and self.lap_times[car_index] else 0,
            },
            delta_to_leader=0.0,
        )

    def get_leader_delta(self, car_index: int) -> float:
        """Calculate delta to leader based on position."""
        if not self.positions:
            return 0.0
        leader_idx = min(self.positions, key=self.positions.get)
        if car_index == leader_idx:
            return 0.0
        leader_best = self.best_lap.get(leader_idx, float("inf"))
        car_best = self.best_lap.get(car_index, float("inf"))
        return round(car_best - leader_best, 3)
