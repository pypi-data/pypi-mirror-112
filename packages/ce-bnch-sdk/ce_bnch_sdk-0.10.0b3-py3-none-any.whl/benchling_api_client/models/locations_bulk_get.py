from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.location import Location

T = TypeVar("T", bound="LocationsBulkGet")


@attr.s(auto_attribs=True)
class LocationsBulkGet:
    """  """

    _locations: List[Location]

    def to_dict(self) -> Dict[str, Any]:
        locations = []
        for locations_item_data in self._locations:
            locations_item = locations_item_data.to_dict()

            locations.append(locations_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "locations": locations,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        locations = []
        _locations = d.pop("locations")
        for locations_item_data in _locations:
            locations_item = Location.from_dict(locations_item_data)

            locations.append(locations_item)

        locations_bulk_get = cls(
            locations=locations,
        )

        return locations_bulk_get

    @property
    def locations(self) -> List[Location]:
        return self._locations

    @locations.setter
    def locations(self, value: List[Location]) -> None:
        self._locations = value
