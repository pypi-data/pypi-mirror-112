from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntriesArchivalChange")


@attr.s(auto_attribs=True)
class EntriesArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of entries that changed.."""

    _entry_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        entry_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._entry_ids, Unset):
            entry_ids = self._entry_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if entry_ids is not UNSET:
            field_dict["entryIds"] = entry_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entry_ids = cast(List[str], d.pop("entryIds", UNSET))

        entries_archival_change = cls(
            entry_ids=entry_ids,
        )

        return entries_archival_change

    @property
    def entry_ids(self) -> List[str]:
        if isinstance(self._entry_ids, Unset):
            raise NotPresentError(self, "entry_ids")
        return self._entry_ids

    @entry_ids.setter
    def entry_ids(self, value: List[str]) -> None:
        self._entry_ids = value

    @entry_ids.deleter
    def entry_ids(self) -> None:
        self._entry_ids = UNSET
