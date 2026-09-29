from collections import defaultdict

# pyrefly: ignore [missing-import]
from models import Event
# pyrefly: ignore [missing-import]
from twin import StateEngine

class SimulationEngine:
    def __init__(self, state_engine: StateEngine) -> None:
        self.state_engine = state_engine
        self.events: dict[int, list[Event]] = defaultdict(list)
    def schedule_event(self, event: Event) -> None:
        self.events[event.timestep].append(event)
    def run_step(self) -> list[Event]:
        timestep = self.state_engine.state.timestep
        scheduled_events = self.events.get(timestep, [])
        processed_events = []
        for event in scheduled_events:
            self._process_event(event)
            processed_events.append(event)
        self.state_engine.advance()
        return processed_events
    def run(self, steps: int) -> list[Event]:
        processed_events: list[Event] = []
        for _ in range(steps):
            processed_events.extend(self.run_step())
        return processed_events
    def _process_event(self, event: Event) -> None:
        if event.type == "state_change":
            self.state_engine.update_node(
                event.target,
                compromised=event.parameters.get("compromised"),
                privilege=event.parameters.get("privilege"),
                status=event.parameters.get("status"),
                source=event.source,
                action=event.action,
            )
        else:
            raise ValueError(
                f"Unsupported event type: {event.type}"
            )