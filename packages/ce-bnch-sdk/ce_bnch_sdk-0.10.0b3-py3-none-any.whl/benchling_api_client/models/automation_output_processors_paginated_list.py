from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.automation_output_processor import AutomationOutputProcessor

T = TypeVar("T", bound="AutomationOutputProcessorsPaginatedList")


@attr.s(auto_attribs=True)
class AutomationOutputProcessorsPaginatedList:
    """ A paginated list of automation output processors which have an attached file. """

    _automation_output_processors: List[AutomationOutputProcessor]
    _next_token: str

    def to_dict(self) -> Dict[str, Any]:
        automation_output_processors = []
        for automation_output_processors_item_data in self._automation_output_processors:
            automation_output_processors_item = automation_output_processors_item_data.to_dict()

            automation_output_processors.append(automation_output_processors_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "automationOutputProcessors": automation_output_processors,
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        automation_output_processors = []
        _automation_output_processors = d.pop("automationOutputProcessors")
        for automation_output_processors_item_data in _automation_output_processors:
            automation_output_processors_item = AutomationOutputProcessor.from_dict(
                automation_output_processors_item_data
            )

            automation_output_processors.append(automation_output_processors_item)

        next_token = d.pop("nextToken")

        automation_output_processors_paginated_list = cls(
            automation_output_processors=automation_output_processors,
            next_token=next_token,
        )

        return automation_output_processors_paginated_list

    @property
    def automation_output_processors(self) -> List[AutomationOutputProcessor]:
        return self._automation_output_processors

    @automation_output_processors.setter
    def automation_output_processors(self, value: List[AutomationOutputProcessor]) -> None:
        self._automation_output_processors = value

    @property
    def next_token(self) -> str:
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value
