"""Sensor model for the simulated industrial-temperature process."""
from pydantic import BaseModel, Field


class SensorReading(BaseModel):
    actual: float
    reported: float
    compromised: bool = False


class TemperatureSensor:
    def __init__(self, spoof_offset: float = 0.0) -> None:
        self.spoof_offset = spoof_offset

    def read(self, actual_temperature: float) -> SensorReading:
        reported = actual_temperature + self.spoof_offset
        return SensorReading(
            actual=round(actual_temperature, 3),
            reported=round(reported, 3),
            compromised=self.spoof_offset != 0.0,
        )

    def spoof(self, offset: float) -> None:
        self.spoof_offset = float(offset)

    def clear_spoof(self) -> None:
        self.spoof_offset = 0.0
