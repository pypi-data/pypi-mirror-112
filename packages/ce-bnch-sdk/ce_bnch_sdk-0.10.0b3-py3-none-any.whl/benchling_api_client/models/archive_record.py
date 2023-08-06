from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="ArchiveRecord")


@attr.s(auto_attribs=True)
class ArchiveRecord:
    """  """

    _reason: str

    def to_dict(self) -> Dict[str, Any]:
        reason = self._reason

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reason = d.pop("reason")

        archive_record = cls(
            reason=reason,
        )

        return archive_record

    @property
    def reason(self) -> str:
        return self._reason

    @reason.setter
    def reason(self, value: str) -> None:
        self._reason = value
