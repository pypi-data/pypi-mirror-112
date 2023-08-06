from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="Pagination")


@attr.s(auto_attribs=True)
class Pagination:
    """  """

    _next_token: str

    def to_dict(self) -> Dict[str, Any]:
        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        pagination = cls(
            next_token=next_token,
        )

        return pagination

    @property
    def next_token(self) -> str:
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value
