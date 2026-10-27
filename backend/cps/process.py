"""A first-order thermal process suitable for repeatable simulations."""
from pydantic import BaseModel


class ProcessState(BaseModel):
    temperature: float = 25.0
    ambient_temperature: float = 25.0


class ThermalProcess:
    def __init__(
        self,
        initial_temperature: float = 25.0,
        ambient_temperature: float = 25.0,
        heating_rate: float = 8.0,
        cooling_coefficient: float = 0.08,
    ) -> None:
        if heating_rate < 0 or cooling_coefficient < 0:
            raise ValueError("heating_rate and cooling_coefficient must be non-negative")
        self.heating_rate = float(heating_rate)
        self.cooling_coefficient = float(cooling_coefficient)
        self.state = ProcessState(
            temperature=float(initial_temperature),
            ambient_temperature=float(ambient_temperature),
        )

    def advance(self, heater_output: float) -> float:
        output = max(0.0, min(1.0, float(heater_output)))
        current = self.state.temperature
        ambient = self.state.ambient_temperature
        next_temperature = current + self.heating_rate * output - self.cooling_coefficient * (current - ambient)
        self.state.temperature = round(next_temperature, 3)
        return self.state.temperature
