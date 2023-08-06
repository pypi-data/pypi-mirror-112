from typing import Any, Dict, Optional, Type, TypeVar

import attr

T = TypeVar("T", bound="Measurement")


@attr.s(auto_attribs=True)
class Measurement:
    """  """

    _units: Optional[str]
    _value: Optional[float]

    def to_dict(self) -> Dict[str, Any]:
        units = self._units
        value = self._value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "units": units,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        units = d.pop("units")

        value = d.pop("value")

        measurement = cls(
            units=units,
            value=value,
        )

        return measurement

    @property
    def units(self) -> Optional[str]:
        return self._units

    @units.setter
    def units(self, value: Optional[str]) -> None:
        self._units = value

    @property
    def value(self) -> Optional[float]:
        return self._value

    @value.setter
    def value(self, value: Optional[float]) -> None:
        self._value = value
