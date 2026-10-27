# pyrefly: ignore [missing-import]
from models import Edge, EdgeType, Node, NodeType
# pyrefly: ignore [missing-import]
from twin import DigitalTwinGraph


def build_industrial_temperature_twin() -> DigitalTwinGraph:
    twin = DigitalTwinGraph()
    nodes = [
        Node(
            id="operator-01",
            name="Operator",
            type=NodeType.USER,
        ),
        Node(
            id="workstation-01",
            name="Operator Workstation",
            type=NodeType.WORKSTATION,
        ),
        Node(
            id="gateway-01",
            name="Industrial Gateway",
            type=NodeType.GATEWAY,
        ),
        Node(
            id="plc-01",
            name="Main PLC",
            type=NodeType.PLC,
        ),
        Node(
            id="sensor-01",
            name="Temperature Sensor",
            type=NodeType.SENSOR,
        ),
        Node(
            id="controller-01",
            name="Temperature Controller",
            type=NodeType.CONTROLLER,
        ),
        Node(
            id="actuator-01",
            name="Heater Actuator",
            type=NodeType.ACTUATOR,
        ),
        Node(
            id="process-01",
            name="Temperature Process",
            type=NodeType.PHYSICAL_PROCESS,
        ),
    ]
    for node in nodes:
        twin.add_node(node)
    edges = [
        Edge(
            source="operator-01",
            target="workstation-01",
            type=EdgeType.NETWORK,
        ),
        Edge(
            source="workstation-01",
            target="gateway-01",
            type=EdgeType.NETWORK,
        ),
        Edge(
            source="gateway-01",
            target="plc-01",
            type=EdgeType.NETWORK,
        ),
        Edge(
            source="sensor-01",
            target="controller-01",
            type=EdgeType.DATA,
        ),
        Edge(
            source="controller-01",
            target="actuator-01",
            type=EdgeType.CONTROL,
        ),
        Edge(
            source="actuator-01",
            target="process-01",
            type=EdgeType.CONTROL,
        ),
        Edge(
            source="process-01",
            target="sensor-01",
            type=EdgeType.DATA,
        ),
        Edge(
            source="plc-01",
            target="controller-01",
            type=EdgeType.CONTROL,
        ),
    ]
    for edge in edges:
        twin.add_edge(edge)
    return twin