# pyrefly: ignore [missing-import]
from pydantic import BaseModel,Field
from .node import Node 

class TwinState(BaseModel):
    timestep:int = 0
    nodes:dict[str,Node] = Field(default_factory=dict)
    def get_node(self,node_id:str) -> Node:
        if node_id not in self.nodes:
            raise KeyError(f"Node '{node_id}' not found")
        return self.nodes[node_id]