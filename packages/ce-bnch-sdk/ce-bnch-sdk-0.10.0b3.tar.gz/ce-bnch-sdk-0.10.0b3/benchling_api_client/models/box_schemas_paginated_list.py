from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.box_schema import BoxSchema

T = TypeVar("T", bound="BoxSchemasPaginatedList")


@attr.s(auto_attribs=True)
class BoxSchemasPaginatedList:
    """  """

    _next_token: str
    _box_schemas: List[BoxSchema]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self._next_token
        box_schemas = []
        for box_schemas_item_data in self._box_schemas:
            box_schemas_item = box_schemas_item_data.to_dict()

            box_schemas.append(box_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "boxSchemas": box_schemas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        box_schemas = []
        _box_schemas = d.pop("boxSchemas")
        for box_schemas_item_data in _box_schemas:
            box_schemas_item = BoxSchema.from_dict(box_schemas_item_data)

            box_schemas.append(box_schemas_item)

        box_schemas_paginated_list = cls(
            next_token=next_token,
            box_schemas=box_schemas,
        )

        return box_schemas_paginated_list

    @property
    def next_token(self) -> str:
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @property
    def box_schemas(self) -> List[BoxSchema]:
        return self._box_schemas

    @box_schemas.setter
    def box_schemas(self, value: List[BoxSchema]) -> None:
        self._box_schemas = value
