from enum import Enum
# pyrefly: ignore [missing-import]
from pydantic import BaseModel,Field

class EdgeType(str,Enum):
    NETWORK = "network"
    DEPENDENCY = "dependency"
    CONTROL = "control"
    DATA = "data"

class Edge(BaseModel):
    source:str
    target:str
    type:EdgeType
    metadata:dict = Field(default_factory=dict)