import datetime
from typing import Any, Dict, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..models.workflow_stage_run_status import WorkflowStageRunStatus

T = TypeVar("T", bound="WorkflowStageRun")


@attr.s(auto_attribs=True)
class WorkflowStageRun:
    """  """

    _created_at: datetime.datetime
    _id: str
    _name: str
    _status: WorkflowStageRunStatus

    def to_dict(self) -> Dict[str, Any]:
        created_at = self._created_at.isoformat()

        id = self._id
        name = self._name
        status = self._status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "createdAt": created_at,
                "id": id,
                "name": name,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = isoparse(d.pop("createdAt"))

        id = d.pop("id")

        name = d.pop("name")

        status = WorkflowStageRunStatus(d.pop("status"))

        workflow_stage_run = cls(
            created_at=created_at,
            id=id,
            name=name,
            status=status,
        )

        return workflow_stage_run

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

    @property
    def status(self) -> WorkflowStageRunStatus:
        return self._status

    @status.setter
    def status(self, value: WorkflowStageRunStatus) -> None:
        self._status = value
