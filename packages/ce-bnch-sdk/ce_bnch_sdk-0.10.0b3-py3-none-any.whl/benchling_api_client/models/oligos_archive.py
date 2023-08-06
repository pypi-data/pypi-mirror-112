from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..models.oligos_archive_reason import OligosArchiveReason

T = TypeVar("T", bound="OligosArchive")


@attr.s(auto_attribs=True)
class OligosArchive:
    """The request body for archiving Oligos."""

    _oligo_ids: List[str]
    _reason: OligosArchiveReason

    def to_dict(self) -> Dict[str, Any]:
        oligo_ids = self._oligo_ids

        reason = self._reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "oligoIds": oligo_ids,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        oligo_ids = cast(List[str], d.pop("oligoIds"))

        reason = OligosArchiveReason(d.pop("reason"))

        oligos_archive = cls(
            oligo_ids=oligo_ids,
            reason=reason,
        )

        return oligos_archive

    @property
    def oligo_ids(self) -> List[str]:
        return self._oligo_ids

    @oligo_ids.setter
    def oligo_ids(self, value: List[str]) -> None:
        self._oligo_ids = value

    @property
    def reason(self) -> OligosArchiveReason:
        return self._reason

    @reason.setter
    def reason(self, value: OligosArchiveReason) -> None:
        self._reason = value
