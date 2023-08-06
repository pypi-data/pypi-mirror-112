from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..models.aa_sequences_archive_reason import AaSequencesArchiveReason

T = TypeVar("T", bound="AaSequencesArchive")


@attr.s(auto_attribs=True)
class AaSequencesArchive:
    """The request body for archiving AA sequences."""

    _aa_sequence_ids: List[str]
    _reason: AaSequencesArchiveReason

    def to_dict(self) -> Dict[str, Any]:
        aa_sequence_ids = self._aa_sequence_ids

        reason = self._reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "aaSequenceIds": aa_sequence_ids,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        aa_sequence_ids = cast(List[str], d.pop("aaSequenceIds"))

        reason = AaSequencesArchiveReason(d.pop("reason"))

        aa_sequences_archive = cls(
            aa_sequence_ids=aa_sequence_ids,
            reason=reason,
        )

        return aa_sequences_archive

    @property
    def aa_sequence_ids(self) -> List[str]:
        return self._aa_sequence_ids

    @aa_sequence_ids.setter
    def aa_sequence_ids(self, value: List[str]) -> None:
        self._aa_sequence_ids = value

    @property
    def reason(self) -> AaSequencesArchiveReason:
        return self._reason

    @reason.setter
    def reason(self, value: AaSequencesArchiveReason) -> None:
        self._reason = value
