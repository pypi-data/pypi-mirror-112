from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="OligosArchivalChange")


@attr.s(auto_attribs=True)
class OligosArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of Oligos along with any IDs of batches that were archived / unarchived."""

    _batch_ids: Union[Unset, List[str]] = UNSET
    _oligo_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        batch_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._batch_ids, Unset):
            batch_ids = self._batch_ids

        oligo_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._oligo_ids, Unset):
            oligo_ids = self._oligo_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if batch_ids is not UNSET:
            field_dict["batchIds"] = batch_ids
        if oligo_ids is not UNSET:
            field_dict["oligoIds"] = oligo_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        batch_ids = cast(List[str], d.pop("batchIds", UNSET))

        oligo_ids = cast(List[str], d.pop("oligoIds", UNSET))

        oligos_archival_change = cls(
            batch_ids=batch_ids,
            oligo_ids=oligo_ids,
        )

        return oligos_archival_change

    @property
    def batch_ids(self) -> List[str]:
        if isinstance(self._batch_ids, Unset):
            raise NotPresentError(self, "batch_ids")
        return self._batch_ids

    @batch_ids.setter
    def batch_ids(self, value: List[str]) -> None:
        self._batch_ids = value

    @batch_ids.deleter
    def batch_ids(self) -> None:
        self._batch_ids = UNSET

    @property
    def oligo_ids(self) -> List[str]:
        if isinstance(self._oligo_ids, Unset):
            raise NotPresentError(self, "oligo_ids")
        return self._oligo_ids

    @oligo_ids.setter
    def oligo_ids(self, value: List[str]) -> None:
        self._oligo_ids = value

    @oligo_ids.deleter
    def oligo_ids(self) -> None:
        self._oligo_ids = UNSET
