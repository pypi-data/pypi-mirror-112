from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseNotePart")


@attr.s(auto_attribs=True)
class BaseNotePart:
    """  """

    _indentation: Union[Unset, int] = 0
    _type: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        indentation = self._indentation
        type = self._type

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if indentation is not UNSET:
            field_dict["indentation"] = indentation
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        indentation = d.pop("indentation", UNSET)

        type = d.pop("type", UNSET)

        base_note_part = cls(
            indentation=indentation,
            type=type,
        )

        return base_note_part

    @property
    def indentation(self) -> int:
        if isinstance(self._indentation, Unset):
            raise NotPresentError(self, "indentation")
        return self._indentation

    @indentation.setter
    def indentation(self, value: int) -> None:
        self._indentation = value

    @indentation.deleter
    def indentation(self) -> None:
        self._indentation = UNSET

    @property
    def type(self) -> str:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: str) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET
