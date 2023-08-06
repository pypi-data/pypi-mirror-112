from typing import Any, cast, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="AaSequencesUnarchive")


@attr.s(auto_attribs=True)
class AaSequencesUnarchive:
    """The request body for unarchiving AA sequences."""

    _aa_sequence_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        aa_sequence_ids = self._aa_sequence_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "aaSequenceIds": aa_sequence_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        aa_sequence_ids = cast(List[str], d.pop("aaSequenceIds"))

        aa_sequences_unarchive = cls(
            aa_sequence_ids=aa_sequence_ids,
        )

        return aa_sequences_unarchive

    @property
    def aa_sequence_ids(self) -> List[str]:
        return self._aa_sequence_ids

    @aa_sequence_ids.setter
    def aa_sequence_ids(self, value: List[str]) -> None:
        self._aa_sequence_ids = value
