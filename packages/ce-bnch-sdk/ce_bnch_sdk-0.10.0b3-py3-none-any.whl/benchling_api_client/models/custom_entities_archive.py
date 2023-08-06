from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..models.custom_entities_archive_reason import CustomEntitiesArchiveReason

T = TypeVar("T", bound="CustomEntitiesArchive")


@attr.s(auto_attribs=True)
class CustomEntitiesArchive:
    """The request body for archiving custom entities."""

    _custom_entity_ids: List[str]
    _reason: CustomEntitiesArchiveReason

    def to_dict(self) -> Dict[str, Any]:
        custom_entity_ids = self._custom_entity_ids

        reason = self._reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "customEntityIds": custom_entity_ids,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        custom_entity_ids = cast(List[str], d.pop("customEntityIds"))

        reason = CustomEntitiesArchiveReason(d.pop("reason"))

        custom_entities_archive = cls(
            custom_entity_ids=custom_entity_ids,
            reason=reason,
        )

        return custom_entities_archive

    @property
    def custom_entity_ids(self) -> List[str]:
        return self._custom_entity_ids

    @custom_entity_ids.setter
    def custom_entity_ids(self, value: List[str]) -> None:
        self._custom_entity_ids = value

    @property
    def reason(self) -> CustomEntitiesArchiveReason:
        return self._reason

    @reason.setter
    def reason(self, value: CustomEntitiesArchiveReason) -> None:
        self._reason = value
