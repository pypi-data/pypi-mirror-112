from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.automation_input_generator import AutomationInputGenerator

T = TypeVar("T", bound="AutomationFileInputsPaginatedList")


@attr.s(auto_attribs=True)
class AutomationFileInputsPaginatedList:
    """  """

    _automation_input_generators: List[AutomationInputGenerator]
    _next_token: str

    def to_dict(self) -> Dict[str, Any]:
        automation_input_generators = []
        for automation_input_generators_item_data in self._automation_input_generators:
            automation_input_generators_item = automation_input_generators_item_data.to_dict()

            automation_input_generators.append(automation_input_generators_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "automationInputGenerators": automation_input_generators,
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        automation_input_generators = []
        _automation_input_generators = d.pop("automationInputGenerators")
        for automation_input_generators_item_data in _automation_input_generators:
            automation_input_generators_item = AutomationInputGenerator.from_dict(
                automation_input_generators_item_data
            )

            automation_input_generators.append(automation_input_generators_item)

        next_token = d.pop("nextToken")

        automation_file_inputs_paginated_list = cls(
            automation_input_generators=automation_input_generators,
            next_token=next_token,
        )

        return automation_file_inputs_paginated_list

    @property
    def automation_input_generators(self) -> List[AutomationInputGenerator]:
        return self._automation_input_generators

    @automation_input_generators.setter
    def automation_input_generators(self, value: List[AutomationInputGenerator]) -> None:
        self._automation_input_generators = value

    @property
    def next_token(self) -> str:
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value
