import datetime
from typing import Any, cast, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="WorkflowSample")


@attr.s(auto_attribs=True)
class WorkflowSample:
    """  """

    _batch_id: str
    _container_ids: List[str]
    _created_at: datetime.datetime
    _id: str
    _name: str

    def to_dict(self) -> Dict[str, Any]:
        batch_id = self._batch_id
        container_ids = self._container_ids

        created_at = self._created_at.isoformat()

        id = self._id
        name = self._name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "batchId": batch_id,
                "containerIds": container_ids,
                "createdAt": created_at,
                "id": id,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        batch_id = d.pop("batchId")

        container_ids = cast(List[str], d.pop("containerIds"))

        created_at = isoparse(d.pop("createdAt"))

        id = d.pop("id")

        name = d.pop("name")

        workflow_sample = cls(
            batch_id=batch_id,
            container_ids=container_ids,
            created_at=created_at,
            id=id,
            name=name,
        )

        return workflow_sample

    @property
    def batch_id(self) -> str:
        return self._batch_id

    @batch_id.setter
    def batch_id(self, value: str) -> None:
        self._batch_id = value

    @property
    def container_ids(self) -> List[str]:
        return self._container_ids

    @container_ids.setter
    def container_ids(self, value: List[str]) -> None:
        self._container_ids = value

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

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
