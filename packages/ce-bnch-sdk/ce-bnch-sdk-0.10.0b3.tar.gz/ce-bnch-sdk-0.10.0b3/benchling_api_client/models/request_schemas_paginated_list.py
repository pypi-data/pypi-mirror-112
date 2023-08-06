from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.request_schema import RequestSchema

T = TypeVar("T", bound="RequestSchemasPaginatedList")


@attr.s(auto_attribs=True)
class RequestSchemasPaginatedList:
    """  """

    _next_token: str
    _request_schemas: List[RequestSchema]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self._next_token
        request_schemas = []
        for request_schemas_item_data in self._request_schemas:
            request_schemas_item = request_schemas_item_data.to_dict()

            request_schemas.append(request_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "requestSchemas": request_schemas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        request_schemas = []
        _request_schemas = d.pop("requestSchemas")
        for request_schemas_item_data in _request_schemas:
            request_schemas_item = RequestSchema.from_dict(request_schemas_item_data)

            request_schemas.append(request_schemas_item)

        request_schemas_paginated_list = cls(
            next_token=next_token,
            request_schemas=request_schemas,
        )

        return request_schemas_paginated_list

    @property
    def next_token(self) -> str:
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @property
    def request_schemas(self) -> List[RequestSchema]:
        return self._request_schemas

    @request_schemas.setter
    def request_schemas(self, value: List[RequestSchema]) -> None:
        self._request_schemas = value
