from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.event import Event

T = TypeVar("T", bound="EventsPaginatedList")


@attr.s(auto_attribs=True)
class EventsPaginatedList:
    """  """

    _events: List[Event]
    _next_token: str

    def to_dict(self) -> Dict[str, Any]:
        events = []
        for events_item_data in self._events:
            events_item = events_item_data.to_dict()

            events.append(events_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "events": events,
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        events = []
        _events = d.pop("events")
        for events_item_data in _events:
            events_item = Event.from_dict(events_item_data)

            events.append(events_item)

        next_token = d.pop("nextToken")

        events_paginated_list = cls(
            events=events,
            next_token=next_token,
        )

        return events_paginated_list

    @property
    def events(self) -> List[Event]:
        return self._events

    @events.setter
    def events(self, value: List[Event]) -> None:
        self._events = value

    @property
    def next_token(self) -> str:
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value
