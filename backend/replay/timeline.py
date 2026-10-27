"""Event timeline utilities for explainable simulation replay."""
from models import Event


class EventTimeline:
    def __init__(self) -> None:
        self._events: list[Event] = []

    def add(self, event: Event) -> None:
        self._events.append(event)
        self._events.sort(key=lambda item: item.timestep)

    def extend(self, events: list[Event]) -> None:
        for event in events:
            self.add(event)

    def at(self, timestep: int) -> list[Event]:
        return [event for event in self._events if event.timestep == timestep]

    def all(self) -> list[Event]:
        return list(self._events)

    def as_dicts(self) -> list[dict]:
        return [event.model_dump(mode="json") for event in self._events]
