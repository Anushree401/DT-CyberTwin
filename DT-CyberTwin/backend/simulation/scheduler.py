"""Small deterministic event scheduler."""
from collections import defaultdict
from models import Event


class EventScheduler:
    def __init__(self) -> None:
        self._events: dict[int, list[Event]] = defaultdict(list)

    def schedule(self, event: Event) -> None:
        self._events[event.timestep].append(event)
        self._events[event.timestep].sort(key=lambda item: (item.source, item.action))

    def pop_at(self, timestep: int) -> list[Event]:
        return self._events.pop(timestep, [])

    def pending(self) -> dict[int, list[Event]]:
        return {step: list(events) for step, events in self._events.items()}
