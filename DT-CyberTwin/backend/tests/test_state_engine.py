# pyrefly: ignore [missing-import]
from models import Node, NodeType, TwinState
# pyrefly: ignore [missing-import]
from twin import StateEngine


def create_test_state() -> TwinState:
    workstation = Node(
        id="workstation-01",
        name="Operator Workstation",
        type=NodeType.WORKSTATION,
    )
    plc = Node(
        id="plc-01",
        name="Main PLC",
        type=NodeType.PLC,
    )
    return TwinState(
        timestep=0,
        nodes={
            workstation.id: workstation,
            plc.id: plc,
        },
    )


def test_update_node_state():
    engine = StateEngine(create_test_state())
    assert engine.get_node("workstation-01").state.compromised is False
    event = engine.update_node(
        "workstation-01",
        compromised=True,
        privilege="user",
        source="attacker",
        action="compromise",
    )
    node = engine.get_node("workstation-01")
    assert node.state.compromised is True
    assert node.state.privilege == "user"
    assert event.target == "workstation-01"
    assert event.action == "compromise"


def test_state_history():
    engine = StateEngine(create_test_state())
    engine.update_node(
        "workstation-01",
        compromised=True,
        source="attacker",
        action="compromise",
    )
    history = engine.get_history()
    assert len(history) == 1
    assert history[0].target == "workstation-01"


def test_advance_timestep():
    engine = StateEngine(create_test_state())
    assert engine.state.timestep == 0
    timestep = engine.advance()
    assert timestep == 1
    assert engine.state.timestep == 1