from typing import Any, Dict, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.archive_record import ArchiveRecord
from ..types import UNSET, Unset

T = TypeVar("T", bound="Folder")


@attr.s(auto_attribs=True)
class Folder:
    """  """

    _id: str
    _archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    _name: Union[Unset, str] = UNSET
    _parent_folder_id: Union[Unset, str] = UNSET
    _project_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._archive_record, Unset):
            archive_record = self._archive_record.to_dict() if self._archive_record else None

        name = self._name
        parent_folder_id = self._parent_folder_id
        project_id = self._project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if name is not UNSET:
            field_dict["name"] = name
        if parent_folder_id is not UNSET:
            field_dict["parentFolderId"] = parent_folder_id
        if project_id is not UNSET:
            field_dict["projectId"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = ArchiveRecord.from_dict(_archive_record)

        name = d.pop("name", UNSET)

        parent_folder_id = d.pop("parentFolderId", UNSET)

        project_id = d.pop("projectId", UNSET)

        folder = cls(
            id=id,
            archive_record=archive_record,
            name=name,
            parent_folder_id=parent_folder_id,
            project_id=project_id,
        )

        return folder

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @property
    def archive_record(self) -> Optional[ArchiveRecord]:
        if isinstance(self._archive_record, Unset):
            raise NotPresentError(self, "archive_record")
        return self._archive_record

    @archive_record.setter
    def archive_record(self, value: Optional[ArchiveRecord]) -> None:
        self._archive_record = value

    @archive_record.deleter
    def archive_record(self) -> None:
        self._archive_record = UNSET

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET

    @property
    def parent_folder_id(self) -> str:
        if isinstance(self._parent_folder_id, Unset):
            raise NotPresentError(self, "parent_folder_id")
        return self._parent_folder_id

    @parent_folder_id.setter
    def parent_folder_id(self, value: str) -> None:
        self._parent_folder_id = value

    @parent_folder_id.deleter
    def parent_folder_id(self) -> None:
        self._parent_folder_id = UNSET

    @property
    def project_id(self) -> str:
        if isinstance(self._project_id, Unset):
            raise NotPresentError(self, "project_id")
        return self._project_id

    @project_id.setter
    def project_id(self, value: str) -> None:
        self._project_id = value

    @project_id.deleter
    def project_id(self) -> None:
        self._project_id = UNSET
