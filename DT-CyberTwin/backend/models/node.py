from enum import Enum
# pyrefly: ignore [missing-import]
from pydantic import BaseModel,Field

class NodeType(str,Enum):
    USER = "user"
    WORKSTATION = "workstation"
    SERVER = "server"
    GATEWAY = "gateway"
    PLC = "plc"
    SENSOR = "sensor"
    CONTROLLER = "controller"
    ACTUATOR = "actuator"
    PHYSICAL_PROCESS = "physcial_process"

class NodeState(BaseModel):
    compromised:bool = False 
    privilege:str = "none"
    status:str = "normal"

class Node(BaseModel):
    id:str
    name:str 
    type:NodeType
    state:NodeState = Field(default_factory=NodeState)
    metadata:dict = Field(default_factory=dict)