from enum import Enum
# pyrefly: ignore [missing-import]
from pydantic import BaseModel,Field

class EventType(str, Enum):
    ATTACK = "attack"
    STATE_CHANGE = "state_change"
    SENSOR_UPDATE = "sensor_update"
    CONTROL_ACTION = "control_action"
    ACTUATOR_ACTION = "actuator_action"
    SYSTEM = "system"


class Event(BaseModel):
    timestep: int
    type: EventType
    source: str
    target: str | None = None
    action: str
    parameters: dict = Field(default_factory=dict)