"""Deterministic discrete-time event engine for the digital twin."""
from collections import defaultdict
from models import Event, EventType
from twin import StateEngine


class SimulationEngine:
    def __init__(self, state_engine: StateEngine) -> None:
        self.state_engine = state_engine
        self.events: dict[int, list[Event]] = defaultdict(list)
        self.processed_events: list[Event] = []

    def schedule_event(self, event: Event) -> None:
        if event.timestep < self.state_engine.state.timestep:
            raise ValueError("Cannot schedule an event in the past")
        self.events[event.timestep].append(event)
        self.events[event.timestep].sort(key=lambda item: (item.source, item.action))

    def run_step(self) -> list[Event]:
        timestep = self.state_engine.state.timestep
        scheduled_events = self.events.pop(timestep, [])
        for event in scheduled_events:
            self._process_event(event)
            self.processed_events.append(event)
        self.state_engine.advance()
        return scheduled_events

    def run(self, steps: int) -> list[Event]:
        if steps < 0:
            raise ValueError("steps must be non-negative")
        processed: list[Event] = []
        for _ in range(steps):
            processed.extend(self.run_step())
        return processed

    def _process_event(self, event: Event) -> None:
        if event.type == EventType.STATE_CHANGE:
            if event.target is None:
                raise ValueError("state_change events require a target")
            self.state_engine.update_node(
                event.target,
                compromised=event.parameters.get("compromised"),
                privilege=event.parameters.get("privilege"),
                status=event.parameters.get("status"),
                timestep=event.timestep,
                source=event.source,
                action=event.action,
            )
            return

        if event.type in {EventType.ATTACK, EventType.SENSOR_UPDATE, EventType.CONTROL_ACTION, EventType.ACTUATOR_ACTION, EventType.SYSTEM}:
            if event.target is not None:
                node = self.state_engine.get_node(event.target)
                node.metadata.setdefault("events", []).append(event.model_dump(mode="json"))
                node.metadata.update({
                    key: value for key, value in event.parameters.items()
                    if key not in {"previous_state", "new_state"}
                })
            return

        raise ValueError(f"Unsupported event type: {event.type}")
