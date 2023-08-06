from typing import Any, Dict, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.container_quantity_units import ContainerQuantityUnits
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerQuantity")


@attr.s(auto_attribs=True)
class ContainerQuantity:
    """ Quantity of a container, well, or transfer. Supports mass, volume, and other quantities. """

    _units: Union[Unset, None, ContainerQuantityUnits] = UNSET
    _value: Union[Unset, None, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        units: Union[Unset, None, int] = UNSET
        if not isinstance(self._units, Unset):
            units = self._units.value if self._units else None

        value = self._value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if units is not UNSET:
            field_dict["units"] = units
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        units = None
        _units = d.pop("units", UNSET)
        if _units is not None and _units is not UNSET:
            units = ContainerQuantityUnits(_units)

        value = d.pop("value", UNSET)

        container_quantity = cls(
            units=units,
            value=value,
        )

        return container_quantity

    @property
    def units(self) -> Optional[ContainerQuantityUnits]:
        if isinstance(self._units, Unset):
            raise NotPresentError(self, "units")
        return self._units

    @units.setter
    def units(self, value: Optional[ContainerQuantityUnits]) -> None:
        self._units = value

    @units.deleter
    def units(self) -> None:
        self._units = UNSET

    @property
    def value(self) -> Optional[float]:
        if isinstance(self._value, Unset):
            raise NotPresentError(self, "value")
        return self._value

    @value.setter
    def value(self, value: Optional[float]) -> None:
        self._value = value

    @value.deleter
    def value(self) -> None:
        self._value = UNSET
