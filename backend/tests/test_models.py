# pyrefly: ignore [missing-import]
from models import (
    Edge, 
    EdgeType,
    Event, 
    EventType,
    Node,
    NodeType,
    TwinState
)

def test_create_node():
    node = Node(
        id="plc-01",
        name="Main PLC",
        type=NodeType.PLC,
    ) 
    assert node.id == "plc-01"
    assert node.type == NodeType.PLC 
    assert node.state.compromised is False 

def test_create_edge():
    edge = Edge(
        source="sensor-01",
        target="plc-01",
        type=EdgeType.CONTROL,
    )
    assert edge.source == "sensor-01"
    assert edge.target == "plc-01"
    assert edge.type == EdgeType.CONTROL

def test_twin_state():
    plc = Node(
        id="plc-01",
        name="Main PLC",
        type=NodeType.PLC,
    )
    state = TwinState(
        timestep=0,
        nodes={"plc-01": plc},
    )
    assert state.get_node("plc-01").name == "Main PLC"

def test_event():
    event = Event(
        timestep=1,
        type=EventType.ATTACK,
        source="attacker",
        target="plc-01",
        action="compromise",
    )
    assert event.timestep == 1
    assert event.target == "plc-01"
    assert event.action == "compromise"
    