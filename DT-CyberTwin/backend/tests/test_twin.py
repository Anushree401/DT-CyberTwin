# pyrefly: ignore [missing-import]
from models import EdgeType, NodeType
# pyrefly: ignore [missing-import]
from scenarios.industrial_temperature import (
    build_industrial_temperature_twin,
)


def test_industrial_twin_topology():
    twin = build_industrial_temperature_twin()
    assert twin.node_count() == 8
    assert twin.edge_count() == 8


def test_plc_exists():
    twin = build_industrial_temperature_twin()
    plc = twin.get_node("plc-01")
    assert plc.name == "Main PLC"
    assert plc.type == NodeType.PLC
    assert plc.state.compromised is False


def test_workstation_to_plc_path():
    twin = build_industrial_temperature_twin()
    graph = twin.graph
    assert nx_path_exists(
        graph,
        "workstation-01",
        "plc-01",
    )


def test_cps_loop_exists():
    twin = build_industrial_temperature_twin()
    assert "controller-01" in twin.neighbors("sensor-01")
    assert "actuator-01" in twin.neighbors("controller-01")
    assert "process-01" in twin.neighbors("actuator-01")
    assert "sensor-01" in twin.neighbors("process-01")


def test_control_edge():
    twin = build_industrial_temperature_twin()
    edge = twin.get_edge(
        "controller-01",
        "actuator-01",
    )
    assert edge.type == EdgeType.CONTROL


def nx_path_exists(graph, source: str, target: str) -> bool:
    import networkx as nx #circular import idk why
    return nx.has_path(graph, source, target)