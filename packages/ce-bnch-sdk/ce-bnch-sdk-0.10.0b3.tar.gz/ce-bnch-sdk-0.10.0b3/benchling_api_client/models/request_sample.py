from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestSample")


@attr.s(auto_attribs=True)
class RequestSample:
    """  """

    _batch_id: Union[Unset, str] = UNSET
    _container_id: Union[Unset, str] = UNSET
    _entity_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        batch_id = self._batch_id
        container_id = self._container_id
        entity_id = self._entity_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if batch_id is not UNSET:
            field_dict["batchId"] = batch_id
        if container_id is not UNSET:
            field_dict["containerId"] = container_id
        if entity_id is not UNSET:
            field_dict["entityId"] = entity_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        batch_id = d.pop("batchId", UNSET)

        container_id = d.pop("containerId", UNSET)

        entity_id = d.pop("entityId", UNSET)

        request_sample = cls(
            batch_id=batch_id,
            container_id=container_id,
            entity_id=entity_id,
        )

        return request_sample

    @property
    def batch_id(self) -> str:
        if isinstance(self._batch_id, Unset):
            raise NotPresentError(self, "batch_id")
        return self._batch_id

    @batch_id.setter
    def batch_id(self, value: str) -> None:
        self._batch_id = value

    @batch_id.deleter
    def batch_id(self) -> None:
        self._batch_id = UNSET

    @property
    def container_id(self) -> str:
        if isinstance(self._container_id, Unset):
            raise NotPresentError(self, "container_id")
        return self._container_id

    @container_id.setter
    def container_id(self, value: str) -> None:
        self._container_id = value

    @container_id.deleter
    def container_id(self) -> None:
        self._container_id = UNSET

    @property
    def entity_id(self) -> str:
        if isinstance(self._entity_id, Unset):
            raise NotPresentError(self, "entity_id")
        return self._entity_id

    @entity_id.setter
    def entity_id(self, value: str) -> None:
        self._entity_id = value

    @entity_id.deleter
    def entity_id(self) -> None:
        self._entity_id = UNSET
