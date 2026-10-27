"""Orchestrates the reference industrial temperature-control scenario."""
from models import Event, EventType, Node, TwinState, SimulationRequest
from scenarios.industrial_temperature import build_industrial_temperature_twin
from twin import StateEngine
from cps.dynamics import TemperatureCPS
from attacks.rules import compromise_node, spoof_sensor
from impact.metrics import calculate_impact_metrics
from impact.propagation import propagate_temperature_impact
from replay.timeline import EventTimeline


def run_industrial_temperature_scenario(request: SimulationRequest) -> dict:
    twin = build_industrial_temperature_twin()
    state = TwinState(nodes={node_id: twin.get_node(node_id) for node_id in twin.graph.nodes})
    state_engine = StateEngine(state)
    cps = TemperatureCPS(
        initial_temperature=request.initial_temperature,
        setpoint=request.setpoint,
    )
    timeline = EventTimeline()
    samples: list[dict] = []

    if request.attack and request.attack_timestep >= request.steps:
        raise ValueError("attack_timestep must be less than steps when attack is enabled")

    for timestep in range(request.steps):
        if request.attack and timestep == request.attack_timestep:
            timeline.add(compromise_node(state_engine, "gateway-01", timestep=timestep, privilege="admin"))
            timeline.add(compromise_node(state_engine, "plc-01", timestep=timestep, privilege="control"))
            spoof_event = spoof_sensor(
                state_engine,
                "sensor-01",
                timestep=timestep,
                offset=request.spoof_offset,
            )
            cps.sensor.spoof(request.spoof_offset)
            timeline.add(spoof_event)
            timeline.add(Event(
                timestep=timestep,
                type=EventType.ATTACK,
                source="simulated_attack",
                target="gateway-01",
                action="attack_path_compromised",
                parameters={"path": ["workstation-01", "gateway-01", "plc-01"]},
            ))

        result = cps.step(timestep)
        sample = result.model_dump()
        samples.append(sample)
        sensor_node = state_engine.get_node("sensor-01")
        sensor_node.metadata.update({
            "actual_temperature": result.actual_temperature,
            "measured_temperature": result.measured_temperature,
            "reported_temperature": result.reported_temperature,
            "last_updated_timestep": timestep,
        })
        controller_node = state_engine.get_node("controller-01")
        controller_node.metadata.update({
            "heater_output": result.heater_output,
            "decision_reason": result.decision_reason,
            "last_updated_timestep": timestep,
        })
        actuator_node = state_engine.get_node("actuator-01")
        actuator_node.metadata.update({"output": result.heater_output, "status": result.actuator_status})
        process_node = state_engine.get_node("process-01")
        process_node.metadata["temperature"] = result.actual_temperature

        timeline.add(Event(
            timestep=timestep,
            type=EventType.SENSOR_UPDATE,
            source="sensor-01",
            target="controller-01",
            action="temperature_reading",
            parameters={
                "actual_temperature_after_step": result.actual_temperature,
                "measured_temperature": result.measured_temperature,
                "reported_temperature": result.reported_temperature,
                "spoofed": result.sensor_compromised,
            },
        ))
        timeline.add(Event(
            timestep=timestep,
            type=EventType.CONTROL_ACTION,
            source="controller-01",
            target="actuator-01",
            action="heater_control_decision",
            parameters={
                "heater_output": result.heater_output,
                "reason": result.decision_reason,
                "reported_temperature": result.reported_temperature,
            },
        ))
        timeline.add(Event(
            timestep=timestep,
            type=EventType.SYSTEM,
            source="process-01",
            action="temperature_advanced",
            parameters={"actual_temperature": result.actual_temperature},
        ))
        state_engine.advance()

    impacts = propagate_temperature_impact(samples, safe_max=request.safe_max)
    metrics = calculate_impact_metrics(
        [sample["actual_temperature"] for sample in samples],
        safe_max=request.safe_max,
        setpoint=request.setpoint,
    )
    return {
        "scenario": "industrial_temperature_control",
        "timesteps": samples,
        "impacts": impacts,
        "metrics": metrics,
        "timeline": timeline.as_dicts(),
        "final_state": {
            node_id: node.model_dump(mode="json") for node_id, node in state_engine.state.nodes.items()
        },
    }
