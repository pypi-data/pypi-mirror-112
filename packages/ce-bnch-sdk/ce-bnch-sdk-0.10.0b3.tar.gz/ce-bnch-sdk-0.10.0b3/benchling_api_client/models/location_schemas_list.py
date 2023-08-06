from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.location_schema import LocationSchema

T = TypeVar("T", bound="LocationSchemasList")


@attr.s(auto_attribs=True)
class LocationSchemasList:
    """  """

    _location_schemas: List[LocationSchema]

    def to_dict(self) -> Dict[str, Any]:
        location_schemas = []
        for location_schemas_item_data in self._location_schemas:
            location_schemas_item = location_schemas_item_data.to_dict()

            location_schemas.append(location_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "locationSchemas": location_schemas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        location_schemas = []
        _location_schemas = d.pop("locationSchemas")
        for location_schemas_item_data in _location_schemas:
            location_schemas_item = LocationSchema.from_dict(location_schemas_item_data)

            location_schemas.append(location_schemas_item)

        location_schemas_list = cls(
            location_schemas=location_schemas,
        )

        return location_schemas_list

    @property
    def location_schemas(self) -> List[LocationSchema]:
        return self._location_schemas

    @location_schemas.setter
    def location_schemas(self, value: List[LocationSchema]) -> None:
        self._location_schemas = value
