from typing import Any, cast, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="AssayResultsCreateResponse")


@attr.s(auto_attribs=True)
class AssayResultsCreateResponse:
    """  """

    _assay_results: List[str]

    def to_dict(self) -> Dict[str, Any]:
        assay_results = self._assay_results

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "assayResults": assay_results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assay_results = cast(List[str], d.pop("assayResults"))

        assay_results_create_response = cls(
            assay_results=assay_results,
        )

        return assay_results_create_response

    @property
    def assay_results(self) -> List[str]:
        return self._assay_results

    @assay_results.setter
    def assay_results(self, value: List[str]) -> None:
        self._assay_results = value
