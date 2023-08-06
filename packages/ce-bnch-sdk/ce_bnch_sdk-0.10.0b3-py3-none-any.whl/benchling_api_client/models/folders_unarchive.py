from typing import Any, cast, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="FoldersUnarchive")


@attr.s(auto_attribs=True)
class FoldersUnarchive:
    """  """

    _folder_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        folder_ids = self._folder_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "folderIds": folder_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        folder_ids = cast(List[str], d.pop("folderIds"))

        folders_unarchive = cls(
            folder_ids=folder_ids,
        )

        return folders_unarchive

    @property
    def folder_ids(self) -> List[str]:
        return self._folder_ids

    @folder_ids.setter
    def folder_ids(self, value: List[str]) -> None:
        self._folder_ids = value
