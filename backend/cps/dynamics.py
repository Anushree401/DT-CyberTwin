"""One deterministic cyber-physical timestep."""
from pydantic import BaseModel
from cps.sensor import TemperatureSensor
from cps.controller import TemperatureController, ControlDecision
from cps.actuator import HeaterActuator, ActuatorState
from cps.process import ThermalProcess


class CPSStepResult(BaseModel):
    timestep: int
    actual_temperature: float
    measured_temperature: float
    reported_temperature: float
    heater_output: float
    actuator_status: str
    decision_reason: str
    sensor_compromised: bool


class TemperatureCPS:
    def __init__(
        self,
        *,
        initial_temperature: float = 25.0,
        setpoint: float = 40.0,
        ambient_temperature: float = 25.0,
        heating_rate: float = 8.0,
        cooling_coefficient: float = 0.08,
    ) -> None:
        self.sensor = TemperatureSensor()
        self.controller = TemperatureController(setpoint=setpoint)
        self.actuator = HeaterActuator()
        self.process = ThermalProcess(
            initial_temperature=initial_temperature,
            ambient_temperature=ambient_temperature,
            heating_rate=heating_rate,
            cooling_coefficient=cooling_coefficient,
        )

    def step(self, timestep: int) -> CPSStepResult:
        measured_temperature = round(self.process.state.temperature, 3)
        reading = self.sensor.read(measured_temperature)
        decision: ControlDecision = self.controller.decide(reading.reported, timestep)
        actuator: ActuatorState = self.actuator.apply(decision.heater_output)
        new_temperature = self.process.advance(actuator.output)
        return CPSStepResult(
            timestep=timestep,
            actual_temperature=new_temperature,
            measured_temperature=measured_temperature,
            reported_temperature=reading.reported,
            heater_output=actuator.output,
            actuator_status=actuator.status,
            decision_reason=decision.reason,
            sensor_compromised=reading.compromised,
        )
