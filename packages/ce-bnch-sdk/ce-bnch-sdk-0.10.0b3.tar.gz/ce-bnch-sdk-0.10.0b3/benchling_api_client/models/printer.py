from typing import Any, Dict, Optional, Type, TypeVar

import attr

T = TypeVar("T", bound="Printer")


@attr.s(auto_attribs=True)
class Printer:
    """  """

    _address: str
    _id: str
    _name: str
    _registry_id: str
    _description: Optional[str]
    _port: Optional[int]

    def to_dict(self) -> Dict[str, Any]:
        address = self._address
        id = self._id
        name = self._name
        registry_id = self._registry_id
        description = self._description
        port = self._port

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "address": address,
                "id": id,
                "name": name,
                "registryId": registry_id,
                "description": description,
                "port": port,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address = d.pop("address")

        id = d.pop("id")

        name = d.pop("name")

        registry_id = d.pop("registryId")

        description = d.pop("description")

        port = d.pop("port")

        printer = cls(
            address=address,
            id=id,
            name=name,
            registry_id=registry_id,
            description=description,
            port=port,
        )

        return printer

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str) -> None:
        self._address = value

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def registry_id(self) -> str:
        return self._registry_id

    @registry_id.setter
    def registry_id(self, value: str) -> None:
        self._registry_id = value

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

    @property
    def port(self) -> Optional[int]:
        return self._port

    @port.setter
    def port(self, value: Optional[int]) -> None:
        self._port = value
