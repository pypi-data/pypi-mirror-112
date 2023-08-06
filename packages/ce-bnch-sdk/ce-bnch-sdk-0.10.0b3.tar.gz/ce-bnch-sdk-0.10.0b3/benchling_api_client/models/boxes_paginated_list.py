from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.box import Box

T = TypeVar("T", bound="BoxesPaginatedList")


@attr.s(auto_attribs=True)
class BoxesPaginatedList:
    """  """

    _boxes: List[Box]
    _next_token: str

    def to_dict(self) -> Dict[str, Any]:
        boxes = []
        for boxes_item_data in self._boxes:
            boxes_item = boxes_item_data.to_dict()

            boxes.append(boxes_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "boxes": boxes,
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        boxes = []
        _boxes = d.pop("boxes")
        for boxes_item_data in _boxes:
            boxes_item = Box.from_dict(boxes_item_data)

            boxes.append(boxes_item)

        next_token = d.pop("nextToken")

        boxes_paginated_list = cls(
            boxes=boxes,
            next_token=next_token,
        )

        return boxes_paginated_list

    @property
    def boxes(self) -> List[Box]:
        return self._boxes

    @boxes.setter
    def boxes(self, value: List[Box]) -> None:
        self._boxes = value

    @property
    def next_token(self) -> str:
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value
