from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="BlobPart")


@attr.s(auto_attribs=True)
class BlobPart:
    """  """

    _e_tag: Union[Unset, str] = UNSET
    _part_number: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        e_tag = self._e_tag
        part_number = self._part_number

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if e_tag is not UNSET:
            field_dict["eTag"] = e_tag
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        e_tag = d.pop("eTag", UNSET)

        part_number = d.pop("partNumber", UNSET)

        blob_part = cls(
            e_tag=e_tag,
            part_number=part_number,
        )

        return blob_part

    @property
    def e_tag(self) -> str:
        if isinstance(self._e_tag, Unset):
            raise NotPresentError(self, "e_tag")
        return self._e_tag

    @e_tag.setter
    def e_tag(self, value: str) -> None:
        self._e_tag = value

    @e_tag.deleter
    def e_tag(self) -> None:
        self._e_tag = UNSET

    @property
    def part_number(self) -> int:
        if isinstance(self._part_number, Unset):
            raise NotPresentError(self, "part_number")
        return self._part_number

    @part_number.setter
    def part_number(self, value: int) -> None:
        self._part_number = value

    @part_number.deleter
    def part_number(self) -> None:
        self._part_number = UNSET
