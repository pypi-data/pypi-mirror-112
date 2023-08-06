from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaTemplateAlignmentFile")


@attr.s(auto_attribs=True)
class DnaTemplateAlignmentFile:
    """  """

    _data: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        data = self._data
        name = self._name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data = d.pop("data", UNSET)

        name = d.pop("name", UNSET)

        dna_template_alignment_file = cls(
            data=data,
            name=name,
        )

        return dna_template_alignment_file

    @property
    def data(self) -> str:
        if isinstance(self._data, Unset):
            raise NotPresentError(self, "data")
        return self._data

    @data.setter
    def data(self, value: str) -> None:
        self._data = value

    @data.deleter
    def data(self) -> None:
        self._data = UNSET

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET
