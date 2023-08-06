from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.aligned_sequence import AlignedSequence
from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaAlignment")


@attr.s(auto_attribs=True)
class DnaAlignment:
    """  """

    _aligned_sequences: Union[Unset, List[AlignedSequence]] = UNSET
    _id: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        aligned_sequences: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._aligned_sequences, Unset):
            aligned_sequences = []
            for aligned_sequences_item_data in self._aligned_sequences:
                aligned_sequences_item = aligned_sequences_item_data.to_dict()

                aligned_sequences.append(aligned_sequences_item)

        id = self._id
        name = self._name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if aligned_sequences is not UNSET:
            field_dict["alignedSequences"] = aligned_sequences
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        aligned_sequences = []
        _aligned_sequences = d.pop("alignedSequences", UNSET)
        for aligned_sequences_item_data in _aligned_sequences or []:
            aligned_sequences_item = AlignedSequence.from_dict(aligned_sequences_item_data)

            aligned_sequences.append(aligned_sequences_item)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        dna_alignment = cls(
            aligned_sequences=aligned_sequences,
            id=id,
            name=name,
        )

        return dna_alignment

    @property
    def aligned_sequences(self) -> List[AlignedSequence]:
        if isinstance(self._aligned_sequences, Unset):
            raise NotPresentError(self, "aligned_sequences")
        return self._aligned_sequences

    @aligned_sequences.setter
    def aligned_sequences(self, value: List[AlignedSequence]) -> None:
        self._aligned_sequences = value

    @aligned_sequences.deleter
    def aligned_sequences(self) -> None:
        self._aligned_sequences = UNSET

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

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
