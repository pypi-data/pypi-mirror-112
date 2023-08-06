from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayRunsBulkCreateResponse")


@attr.s(auto_attribs=True)
class AssayRunsBulkCreateResponse:
    """  """

    _assay_runs: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        assay_runs: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._assay_runs, Unset):
            assay_runs = self._assay_runs

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if assay_runs is not UNSET:
            field_dict["assayRuns"] = assay_runs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assay_runs = cast(List[str], d.pop("assayRuns", UNSET))

        assay_runs_bulk_create_response = cls(
            assay_runs=assay_runs,
        )

        return assay_runs_bulk_create_response

    @property
    def assay_runs(self) -> List[str]:
        if isinstance(self._assay_runs, Unset):
            raise NotPresentError(self, "assay_runs")
        return self._assay_runs

    @assay_runs.setter
    def assay_runs(self, value: List[str]) -> None:
        self._assay_runs = value

    @assay_runs.deleter
    def assay_runs(self) -> None:
        self._assay_runs = UNSET
