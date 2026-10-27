"""Simple deterministic on/off temperature controller."""
from pydantic import BaseModel, Field


class ControlDecision(BaseModel):
    timestep: int
    measured_temperature: float
    setpoint: float
    heater_output: float
    reason: str


class TemperatureController:
    def __init__(self, setpoint: float = 40.0, deadband: float = 1.0) -> None:
        if deadband < 0:
            raise ValueError("deadband must be non-negative")
        self.setpoint = float(setpoint)
        self.deadband = float(deadband)

    def decide(self, measured_temperature: float, timestep: int) -> ControlDecision:
        if measured_temperature < self.setpoint - self.deadband:
            output, reason = 1.0, "temperature_below_setpoint"
        elif measured_temperature > self.setpoint + self.deadband:
            output, reason = 0.0, "temperature_above_setpoint"
        else:
            # Retain the safe, deterministic off state inside the deadband.
            output, reason = 0.0, "temperature_within_deadband"
        return ControlDecision(
            timestep=timestep,
            measured_temperature=round(float(measured_temperature), 3),
            setpoint=self.setpoint,
            heater_output=output,
            reason=reason,
        )
