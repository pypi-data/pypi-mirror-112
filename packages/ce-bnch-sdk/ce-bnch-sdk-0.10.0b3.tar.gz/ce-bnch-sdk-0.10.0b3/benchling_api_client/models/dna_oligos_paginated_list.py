from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.dna_oligo import DnaOligo

T = TypeVar("T", bound="DnaOligosPaginatedList")


@attr.s(auto_attribs=True)
class DnaOligosPaginatedList:
    """  """

    _dna_oligos: List[DnaOligo]
    _next_token: str

    def to_dict(self) -> Dict[str, Any]:
        dna_oligos = []
        for dna_oligos_item_data in self._dna_oligos:
            dna_oligos_item = dna_oligos_item_data.to_dict()

            dna_oligos.append(dna_oligos_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "dnaOligos": dna_oligos,
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dna_oligos = []
        _dna_oligos = d.pop("dnaOligos")
        for dna_oligos_item_data in _dna_oligos:
            dna_oligos_item = DnaOligo.from_dict(dna_oligos_item_data)

            dna_oligos.append(dna_oligos_item)

        next_token = d.pop("nextToken")

        dna_oligos_paginated_list = cls(
            dna_oligos=dna_oligos,
            next_token=next_token,
        )

        return dna_oligos_paginated_list

    @property
    def dna_oligos(self) -> List[DnaOligo]:
        return self._dna_oligos

    @dna_oligos.setter
    def dna_oligos(self, value: List[DnaOligo]) -> None:
        self._dna_oligos = value

    @property
    def next_token(self) -> str:
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value
