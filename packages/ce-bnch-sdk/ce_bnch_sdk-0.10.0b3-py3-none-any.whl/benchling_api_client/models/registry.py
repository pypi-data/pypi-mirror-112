from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.organization import Organization
from ..types import UNSET, Unset

T = TypeVar("T", bound="Registry")


@attr.s(auto_attribs=True)
class Registry:
    """  """

    _id: str
    _name: Union[Unset, str] = UNSET
    _owner: Union[Unset, Organization] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        name = self._name
        owner: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._owner, Unset):
            owner = self._owner.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if owner is not UNSET:
            field_dict["owner"] = owner

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name", UNSET)

        owner: Union[Unset, Organization] = UNSET
        _owner = d.pop("owner", UNSET)
        if not isinstance(_owner, Unset):
            owner = Organization.from_dict(_owner)

        registry = cls(
            id=id,
            name=name,
            owner=owner,
        )

        return registry

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET

    @property
    def owner(self) -> Organization:
        if isinstance(self._owner, Unset):
            raise NotPresentError(self, "owner")
        return self._owner

    @owner.setter
    def owner(self, value: Organization) -> None:
        self._owner = value

    @owner.deleter
    def owner(self) -> None:
        self._owner = UNSET
