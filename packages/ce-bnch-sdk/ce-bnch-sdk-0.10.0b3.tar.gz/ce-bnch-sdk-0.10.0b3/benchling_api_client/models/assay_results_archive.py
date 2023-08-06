from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.assay_results_archive_reason import AssayResultsArchiveReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayResultsArchive")


@attr.s(auto_attribs=True)
class AssayResultsArchive:
    """  """

    _assay_result_ids: List[str]
    _reason: Union[Unset, AssayResultsArchiveReason] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        assay_result_ids = self._assay_result_ids

        reason: Union[Unset, int] = UNSET
        if not isinstance(self._reason, Unset):
            reason = self._reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "assayResultIds": assay_result_ids,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assay_result_ids = cast(List[str], d.pop("assayResultIds"))

        reason = None
        _reason = d.pop("reason", UNSET)
        if _reason is not None and _reason is not UNSET:
            reason = AssayResultsArchiveReason(_reason)

        assay_results_archive = cls(
            assay_result_ids=assay_result_ids,
            reason=reason,
        )

        assay_results_archive.additional_properties = d
        return assay_results_archive

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def assay_result_ids(self) -> List[str]:
        return self._assay_result_ids

    @assay_result_ids.setter
    def assay_result_ids(self, value: List[str]) -> None:
        self._assay_result_ids = value

    @property
    def reason(self) -> AssayResultsArchiveReason:
        if isinstance(self._reason, Unset):
            raise NotPresentError(self, "reason")
        return self._reason

    @reason.setter
    def reason(self, value: AssayResultsArchiveReason) -> None:
        self._reason = value

    @reason.deleter
    def reason(self) -> None:
        self._reason = UNSET
