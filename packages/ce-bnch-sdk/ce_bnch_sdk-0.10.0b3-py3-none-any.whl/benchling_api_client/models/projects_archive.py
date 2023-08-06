from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..models.projects_archive_reason import ProjectsArchiveReason

T = TypeVar("T", bound="ProjectsArchive")


@attr.s(auto_attribs=True)
class ProjectsArchive:
    """  """

    _project_ids: List[str]
    _reason: ProjectsArchiveReason

    def to_dict(self) -> Dict[str, Any]:
        project_ids = self._project_ids

        reason = self._reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "projectIds": project_ids,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_ids = cast(List[str], d.pop("projectIds"))

        reason = ProjectsArchiveReason(d.pop("reason"))

        projects_archive = cls(
            project_ids=project_ids,
            reason=reason,
        )

        return projects_archive

    @property
    def project_ids(self) -> List[str]:
        return self._project_ids

    @project_ids.setter
    def project_ids(self, value: List[str]) -> None:
        self._project_ids = value

    @property
    def reason(self) -> ProjectsArchiveReason:
        return self._reason

    @reason.setter
    def reason(self, value: ProjectsArchiveReason) -> None:
        self._reason = value
