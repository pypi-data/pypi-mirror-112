from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.batch_schema import BatchSchema

T = TypeVar("T", bound="BatchSchemasPaginatedList")


@attr.s(auto_attribs=True)
class BatchSchemasPaginatedList:
    """  """

    _next_token: str
    _batch_schemas: List[BatchSchema]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self._next_token
        batch_schemas = []
        for batch_schemas_item_data in self._batch_schemas:
            batch_schemas_item = batch_schemas_item_data.to_dict()

            batch_schemas.append(batch_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "batchSchemas": batch_schemas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        batch_schemas = []
        _batch_schemas = d.pop("batchSchemas")
        for batch_schemas_item_data in _batch_schemas:
            batch_schemas_item = BatchSchema.from_dict(batch_schemas_item_data)

            batch_schemas.append(batch_schemas_item)

        batch_schemas_paginated_list = cls(
            next_token=next_token,
            batch_schemas=batch_schemas,
        )

        return batch_schemas_paginated_list

    @property
    def next_token(self) -> str:
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @property
    def batch_schemas(self) -> List[BatchSchema]:
        return self._batch_schemas

    @batch_schemas.setter
    def batch_schemas(self, value: List[BatchSchema]) -> None:
        self._batch_schemas = value
