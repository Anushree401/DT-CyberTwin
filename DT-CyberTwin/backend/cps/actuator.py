"""Bounded heater actuator model."""
from pydantic import BaseModel


class ActuatorState(BaseModel):
    output: float = 0.0
    status: str = "off"


class HeaterActuator:
    def __init__(self) -> None:
        self.state = ActuatorState()

    def apply(self, output: float) -> ActuatorState:
        bounded = max(0.0, min(1.0, float(output)))
        self.state = ActuatorState(output=bounded, status="on" if bounded > 0 else "off")
        return self.state.model_copy(deep=True)
