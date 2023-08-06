import datetime
from typing import Any, Dict, Optional, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..models.sample_group import SampleGroup
from ..models.sample_group_status import SampleGroupStatus

T = TypeVar("T", bound="RequestFulfillment")


@attr.s(auto_attribs=True)
class RequestFulfillment:
    """A request fulfillment represents work that is done which changes the status of a request or a sample group within that request.
    Fulfillments are created when state changes between IN_PROGRESS, COMPLETED, or FAILED statuses. Fulfillments do not capture a PENDING state because all requests or request sample groups are considered PENDING until the first corresponding fulfillment is created.
    """

    _created_at: datetime.datetime
    _entry_id: str
    _id: str
    _request_id: str
    _status: SampleGroupStatus
    _sample_group: Optional[SampleGroup]

    def to_dict(self) -> Dict[str, Any]:
        created_at = self._created_at.isoformat()

        entry_id = self._entry_id
        id = self._id
        request_id = self._request_id
        status = self._status.value

        sample_group = self._sample_group.to_dict() if self._sample_group else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "createdAt": created_at,
                "entryId": entry_id,
                "id": id,
                "requestId": request_id,
                "status": status,
                "sampleGroup": sample_group,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = isoparse(d.pop("createdAt"))

        entry_id = d.pop("entryId")

        id = d.pop("id")

        request_id = d.pop("requestId")

        status = SampleGroupStatus(d.pop("status"))

        sample_group = None
        _sample_group = d.pop("sampleGroup")
        if _sample_group is not None:
            sample_group = SampleGroup.from_dict(_sample_group)

        request_fulfillment = cls(
            created_at=created_at,
            entry_id=entry_id,
            id=id,
            request_id=request_id,
            status=status,
            sample_group=sample_group,
        )

        return request_fulfillment

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

    @property
    def entry_id(self) -> str:
        return self._entry_id

    @entry_id.setter
    def entry_id(self, value: str) -> None:
        self._entry_id = value

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @property
    def request_id(self) -> str:
        return self._request_id

    @request_id.setter
    def request_id(self, value: str) -> None:
        self._request_id = value

    @property
    def status(self) -> SampleGroupStatus:
        return self._status

    @status.setter
    def status(self, value: SampleGroupStatus) -> None:
        self._status = value

    @property
    def sample_group(self) -> Optional[SampleGroup]:
        return self._sample_group

    @sample_group.setter
    def sample_group(self, value: Optional[SampleGroup]) -> None:
        self._sample_group = value
