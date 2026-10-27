from models import Node, NodeType, TwinState
from twin import StateEngine
from attacks.rules import compromise_node, spoof_sensor


def test_compromise_node_updates_state_and_history():
    node = Node(id="plc-01", name="PLC", type=NodeType.PLC)
    engine = StateEngine(TwinState(nodes={node.id: node}))
    event = compromise_node(engine, node.id, timestep=2, privilege="control")
    assert engine.get_node(node.id).state.compromised is True
    assert engine.get_node(node.id).state.privilege == "control"
    assert event.action == "simulated_compromise"


def test_spoof_sensor_records_offset():
    node = Node(id="sensor-01", name="Sensor", type=NodeType.SENSOR)
    engine = StateEngine(TwinState(nodes={node.id: node}))
    event = spoof_sensor(engine, node.id, timestep=1, offset=-15)
    assert engine.get_node(node.id).metadata["spoof_offset"] == -15
    assert event.parameters["offset"] == -15
