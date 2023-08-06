from typing import Any, cast, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="PlatesUnarchive")


@attr.s(auto_attribs=True)
class PlatesUnarchive:
    """  """

    _plate_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        plate_ids = self._plate_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "plateIds": plate_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        plate_ids = cast(List[str], d.pop("plateIds"))

        plates_unarchive = cls(
            plate_ids=plate_ids,
        )

        return plates_unarchive

    @property
    def plate_ids(self) -> List[str]:
        return self._plate_ids

    @plate_ids.setter
    def plate_ids(self, value: List[str]) -> None:
        self._plate_ids = value
