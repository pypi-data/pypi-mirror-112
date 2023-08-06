from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestTasksBulkCreate")


@attr.s(auto_attribs=True)
class RequestTasksBulkCreate:
    """  """

    _schema_id: str
    _fields: Union[Unset, Fields] = UNSET
    _sample_group_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        schema_id = self._schema_id
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._fields, Unset):
            fields = self._fields.to_dict()

        sample_group_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._sample_group_ids, Unset):
            sample_group_ids = self._sample_group_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "schemaId": schema_id,
            }
        )
        if fields is not UNSET:
            field_dict["fields"] = fields
        if sample_group_ids is not UNSET:
            field_dict["sampleGroupIds"] = sample_group_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        schema_id = d.pop("schemaId")

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        sample_group_ids = cast(List[str], d.pop("sampleGroupIds", UNSET))

        request_tasks_bulk_create = cls(
            schema_id=schema_id,
            fields=fields,
            sample_group_ids=sample_group_ids,
        )

        return request_tasks_bulk_create

    @property
    def schema_id(self) -> str:
        return self._schema_id

    @schema_id.setter
    def schema_id(self, value: str) -> None:
        self._schema_id = value

    @property
    def fields(self) -> Fields:
        if isinstance(self._fields, Unset):
            raise NotPresentError(self, "fields")
        return self._fields

    @fields.setter
    def fields(self, value: Fields) -> None:
        self._fields = value

    @fields.deleter
    def fields(self) -> None:
        self._fields = UNSET

    @property
    def sample_group_ids(self) -> List[str]:
        if isinstance(self._sample_group_ids, Unset):
            raise NotPresentError(self, "sample_group_ids")
        return self._sample_group_ids

    @sample_group_ids.setter
    def sample_group_ids(self, value: List[str]) -> None:
        self._sample_group_ids = value

    @sample_group_ids.deleter
    def sample_group_ids(self) -> None:
        self._sample_group_ids = UNSET
