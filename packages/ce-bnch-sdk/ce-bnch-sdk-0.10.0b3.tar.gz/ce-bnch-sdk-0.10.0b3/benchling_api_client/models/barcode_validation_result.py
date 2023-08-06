from typing import Any, Dict, Optional, Type, TypeVar

import attr

T = TypeVar("T", bound="BarcodeValidationResult")


@attr.s(auto_attribs=True)
class BarcodeValidationResult:
    """  """

    _barcode: str
    _is_valid: bool
    _message: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        barcode = self._barcode
        is_valid = self._is_valid
        message = self._message

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "barcode": barcode,
                "isValid": is_valid,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        barcode = d.pop("barcode")

        is_valid = d.pop("isValid")

        message = d.pop("message")

        barcode_validation_result = cls(
            barcode=barcode,
            is_valid=is_valid,
            message=message,
        )

        return barcode_validation_result

    @property
    def barcode(self) -> str:
        return self._barcode

    @barcode.setter
    def barcode(self, value: str) -> None:
        self._barcode = value

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @is_valid.setter
    def is_valid(self, value: bool) -> None:
        self._is_valid = value

    @property
    def message(self) -> Optional[str]:
        return self._message

    @message.setter
    def message(self, value: Optional[str]) -> None:
        self._message = value
