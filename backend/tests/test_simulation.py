# pyrefly: ignore [missing-import]
from models import Event, EventType, Node, NodeType, TwinState
# pyrefly: ignore [missing-import]
from simulation import SimulationEngine
# pyrefly: ignore [missing-import]
from twin import StateEngine


def create_test_engine() -> SimulationEngine:
    workstation = Node(
        id="workstation-01",
        name="Operator Workstation",
        type=NodeType.WORKSTATION,
    )
    state = TwinState(
        timestep=0,
        nodes={
            workstation.id: workstation,
        },
    )
    state_engine = StateEngine(state)
    return SimulationEngine(state_engine)


def test_schedule_event():
    engine = create_test_engine()
    event = Event(
        timestep=0,
        type=EventType.STATE_CHANGE,
        source="attacker",
        target="workstation-01",
        action="compromise",
        parameters={
            "compromised": True,
            "privilege": "user",
        },
    )
    engine.schedule_event(event)
    assert len(engine.events[0]) == 1


def test_run_step_processes_event():
    engine = create_test_engine()
    event = Event(
        timestep=0,
        type=EventType.STATE_CHANGE,
        source="attacker",
        target="workstation-01",
        action="compromise",
        parameters={
            "compromised": True,
            "privilege": "user",
        },
    )
    engine.schedule_event(event)
    processed = engine.run_step()
    node = engine.state_engine.get_node("workstation-01")
    assert len(processed) == 1
    assert node.state.compromised is True
    assert node.state.privilege == "user"
    assert engine.state_engine.state.timestep == 1


def test_run_multiple_steps():
    engine = create_test_engine()
    event = Event(
        timestep=2,
        type=EventType.STATE_CHANGE,
        source="attacker",
        target="workstation-01",
        action="compromise",
        parameters={
            "compromised": True,
        },
    )
    engine.schedule_event(event)
    processed = engine.run(3)
    node = engine.state_engine.get_node("workstation-01")
    assert len(processed) == 1
    assert node.state.compromised is True
    assert engine.state_engine.state.timestep == 3