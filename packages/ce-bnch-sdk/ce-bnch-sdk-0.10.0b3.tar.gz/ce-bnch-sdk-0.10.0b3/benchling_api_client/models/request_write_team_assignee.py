from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="RequestWriteTeamAssignee")


@attr.s(auto_attribs=True)
class RequestWriteTeamAssignee:
    """  """

    _team_id: str

    def to_dict(self) -> Dict[str, Any]:
        team_id = self._team_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "teamId": team_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        team_id = d.pop("teamId")

        request_write_team_assignee = cls(
            team_id=team_id,
        )

        return request_write_team_assignee

    @property
    def team_id(self) -> str:
        return self._team_id

    @team_id.setter
    def team_id(self, value: str) -> None:
        self._team_id = value
