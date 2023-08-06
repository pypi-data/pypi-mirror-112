from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.batch import Batch

T = TypeVar("T", bound="BatchesPaginatedList")


@attr.s(auto_attribs=True)
class BatchesPaginatedList:
    """  """

    _batches: List[Batch]
    _next_token: str

    def to_dict(self) -> Dict[str, Any]:
        batches = []
        for batches_item_data in self._batches:
            batches_item = batches_item_data.to_dict()

            batches.append(batches_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "batches": batches,
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        batches = []
        _batches = d.pop("batches")
        for batches_item_data in _batches:
            batches_item = Batch.from_dict(batches_item_data)

            batches.append(batches_item)

        next_token = d.pop("nextToken")

        batches_paginated_list = cls(
            batches=batches,
            next_token=next_token,
        )

        return batches_paginated_list

    @property
    def batches(self) -> List[Batch]:
        return self._batches

    @batches.setter
    def batches(self, value: List[Batch]) -> None:
        self._batches = value

    @property
    def next_token(self) -> str:
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value
