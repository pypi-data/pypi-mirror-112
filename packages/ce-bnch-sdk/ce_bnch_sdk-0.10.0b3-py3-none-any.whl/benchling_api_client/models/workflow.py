import datetime
from typing import Any, Dict, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="Workflow")


@attr.s(auto_attribs=True)
class Workflow:
    """  """

    _created_at: datetime.datetime
    _description: str
    _display_id: str
    _id: str
    _name: str
    _project_id: str

    def to_dict(self) -> Dict[str, Any]:
        created_at = self._created_at.isoformat()

        description = self._description
        display_id = self._display_id
        id = self._id
        name = self._name
        project_id = self._project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "createdAt": created_at,
                "description": description,
                "displayId": display_id,
                "id": id,
                "name": name,
                "projectId": project_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = isoparse(d.pop("createdAt"))

        description = d.pop("description")

        display_id = d.pop("displayId")

        id = d.pop("id")

        name = d.pop("name")

        project_id = d.pop("projectId")

        workflow = cls(
            created_at=created_at,
            description=description,
            display_id=display_id,
            id=id,
            name=name,
            project_id=project_id,
        )

        return workflow

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def display_id(self) -> str:
        return self._display_id

    @display_id.setter
    def display_id(self, value: str) -> None:
        self._display_id = value

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
    def project_id(self) -> str:
        return self._project_id

    @project_id.setter
    def project_id(self, value: str) -> None:
        self._project_id = value
