from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.container_schema import ContainerSchema

T = TypeVar("T", bound="ContainerSchemasPaginatedList")


@attr.s(auto_attribs=True)
class ContainerSchemasPaginatedList:
    """  """

    _next_token: str
    _container_schemas: List[ContainerSchema]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self._next_token
        container_schemas = []
        for container_schemas_item_data in self._container_schemas:
            container_schemas_item = container_schemas_item_data.to_dict()

            container_schemas.append(container_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "containerSchemas": container_schemas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        container_schemas = []
        _container_schemas = d.pop("containerSchemas")
        for container_schemas_item_data in _container_schemas:
            container_schemas_item = ContainerSchema.from_dict(container_schemas_item_data)

            container_schemas.append(container_schemas_item)

        container_schemas_paginated_list = cls(
            next_token=next_token,
            container_schemas=container_schemas,
        )

        return container_schemas_paginated_list

    @property
    def next_token(self) -> str:
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @property
    def container_schemas(self) -> List[ContainerSchema]:
        return self._container_schemas

    @container_schemas.setter
    def container_schemas(self, value: List[ContainerSchema]) -> None:
        self._container_schemas = value
