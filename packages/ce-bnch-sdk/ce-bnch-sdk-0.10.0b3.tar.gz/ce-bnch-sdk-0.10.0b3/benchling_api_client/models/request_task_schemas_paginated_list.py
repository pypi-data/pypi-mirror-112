from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.request_task_schema import RequestTaskSchema

T = TypeVar("T", bound="RequestTaskSchemasPaginatedList")


@attr.s(auto_attribs=True)
class RequestTaskSchemasPaginatedList:
    """  """

    _next_token: str
    _request_task_schemas: List[RequestTaskSchema]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self._next_token
        request_task_schemas = []
        for request_task_schemas_item_data in self._request_task_schemas:
            request_task_schemas_item = request_task_schemas_item_data.to_dict()

            request_task_schemas.append(request_task_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "requestTaskSchemas": request_task_schemas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        request_task_schemas = []
        _request_task_schemas = d.pop("requestTaskSchemas")
        for request_task_schemas_item_data in _request_task_schemas:
            request_task_schemas_item = RequestTaskSchema.from_dict(request_task_schemas_item_data)

            request_task_schemas.append(request_task_schemas_item)

        request_task_schemas_paginated_list = cls(
            next_token=next_token,
            request_task_schemas=request_task_schemas,
        )

        return request_task_schemas_paginated_list

    @property
    def next_token(self) -> str:
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @property
    def request_task_schemas(self) -> List[RequestTaskSchema]:
        return self._request_task_schemas

    @request_task_schemas.setter
    def request_task_schemas(self, value: List[RequestTaskSchema]) -> None:
        self._request_task_schemas = value
