"""Safe, simulated attack rules. These mutate only the in-memory digital twin."""
from models import Event, EventType
from twin import StateEngine


def compromise_node(state_engine: StateEngine, node_id: str, *, timestep: int, privilege: str = "user") -> Event:
    """Mark a simulated asset compromised; no real system is contacted."""
    return state_engine.update_node(
        node_id,
        compromised=True,
        privilege=privilege,
        status="compromised",
        timestep=timestep,
        source="simulated_attack",
        action="simulated_compromise",
    )


def spoof_sensor(state_engine: StateEngine, sensor_id: str, *, timestep: int, offset: float) -> Event:
    """Record a simulated sensor spoofing event on a sensor node."""
    node = state_engine.get_node(sensor_id)
    node.metadata["spoof_offset"] = float(offset)
    node.metadata["sensor_spoof_active"] = True
    return Event(
        timestep=timestep,
        type=EventType.ATTACK,
        source="simulated_attack",
        target=sensor_id,
        action="sensor_spoofing_started",
        parameters={"offset": float(offset), "unit": "temperature_units"},
    )


def stop_sensor_spoof(state_engine: StateEngine, sensor_id: str, *, timestep: int) -> Event:
    node = state_engine.get_node(sensor_id)
    node.metadata["spoof_offset"] = 0.0
    node.metadata["sensor_spoof_active"] = False
    return Event(
        timestep=timestep,
        type=EventType.ATTACK,
        source="simulation",
        target=sensor_id,
        action="sensor_spoofing_stopped",
    )
