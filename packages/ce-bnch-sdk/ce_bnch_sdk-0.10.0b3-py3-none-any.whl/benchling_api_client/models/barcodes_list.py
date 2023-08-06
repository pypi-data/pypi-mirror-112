from typing import Any, cast, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BarcodesList")


@attr.s(auto_attribs=True)
class BarcodesList:
    """  """

    _barcodes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        barcodes = self._barcodes

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "barcodes": barcodes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        barcodes = cast(List[str], d.pop("barcodes"))

        barcodes_list = cls(
            barcodes=barcodes,
        )

        return barcodes_list

    @property
    def barcodes(self) -> List[str]:
        return self._barcodes

    @barcodes.setter
    def barcodes(self, value: List[str]) -> None:
        self._barcodes = value
