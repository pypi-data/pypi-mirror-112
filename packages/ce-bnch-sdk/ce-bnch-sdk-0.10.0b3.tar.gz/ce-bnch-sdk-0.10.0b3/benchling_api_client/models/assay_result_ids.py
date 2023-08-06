from typing import Any, cast, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="AssayResultIds")


@attr.s(auto_attribs=True)
class AssayResultIds:
    """  """

    _assay_result_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        assay_result_ids = self._assay_result_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "assayResultIds": assay_result_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assay_result_ids = cast(List[str], d.pop("assayResultIds"))

        assay_result_ids = cls(
            assay_result_ids=assay_result_ids,
        )

        return assay_result_ids

    @property
    def assay_result_ids(self) -> List[str]:
        return self._assay_result_ids

    @assay_result_ids.setter
    def assay_result_ids(self, value: List[str]) -> None:
        self._assay_result_ids = value
