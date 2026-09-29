from copy import deepcopy
# pyrefly: ignore [missing-import]
from models import Event,Node,TwinState 

class StateEngine:
    def __init__(self,initial_state:TwinState) -> None:
        self.state = initial_state
        self.history:list[Event] = []
    def get_node(self,node_id:str) -> Node:
        return self.state.get_node(node_id)
    def update_node(
        self,node_id:str,
        *,
        compromised: bool | None = None,
        privilege: str | None = None,
        status: str | None = None,
        timestep: int | None = None,
        source: str = "system",
        action: str = "state_update",) -> Event:
        node = self.get_node(node_id)
        previous_state = deepcopy(node.state)
        if compromised is not None:
            node.state.compromised = compromised
        if privilege is not None:
            node.state.privilege = privilege
        if status is not None:
            node.state.status = status
        if timestep is not None:
            self.state.timestep = timestep
        event = Event(
            timestep=self.state.timestep,
            type="state_change",
            source=source,
            target=node_id,
            action=action,
            parameters={
                "previous_state": previous_state.model_dump(),
                "new_state": node.state.model_dump(),
            },
        )
        self.history.append(event)
        return event 
    def advance(self) -> int:
        self.state.timestep += 1
        return self.state.timestep
    def get_history(self) -> list[Event]:
        return list(self.history)