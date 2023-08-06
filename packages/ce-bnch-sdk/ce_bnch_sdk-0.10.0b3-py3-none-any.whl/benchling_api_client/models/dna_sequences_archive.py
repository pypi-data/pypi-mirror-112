from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..models.dna_sequences_archive_reason import DnaSequencesArchiveReason

T = TypeVar("T", bound="DnaSequencesArchive")


@attr.s(auto_attribs=True)
class DnaSequencesArchive:
    """The request body for archiving DNA sequences."""

    _dna_sequence_ids: List[str]
    _reason: DnaSequencesArchiveReason

    def to_dict(self) -> Dict[str, Any]:
        dna_sequence_ids = self._dna_sequence_ids

        reason = self._reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "dnaSequenceIds": dna_sequence_ids,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dna_sequence_ids = cast(List[str], d.pop("dnaSequenceIds"))

        reason = DnaSequencesArchiveReason(d.pop("reason"))

        dna_sequences_archive = cls(
            dna_sequence_ids=dna_sequence_ids,
            reason=reason,
        )

        return dna_sequences_archive

    @property
    def dna_sequence_ids(self) -> List[str]:
        return self._dna_sequence_ids

    @dna_sequence_ids.setter
    def dna_sequence_ids(self, value: List[str]) -> None:
        self._dna_sequence_ids = value

    @property
    def reason(self) -> DnaSequencesArchiveReason:
        return self._reason

    @reason.setter
    def reason(self, value: DnaSequencesArchiveReason) -> None:
        self._reason = value
