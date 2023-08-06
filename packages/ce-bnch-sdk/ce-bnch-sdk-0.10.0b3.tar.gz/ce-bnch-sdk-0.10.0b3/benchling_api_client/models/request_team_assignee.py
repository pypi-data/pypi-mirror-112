from typing import Any, Dict, Type, TypeVar

import attr

from ..models.team_summary import TeamSummary

T = TypeVar("T", bound="RequestTeamAssignee")


@attr.s(auto_attribs=True)
class RequestTeamAssignee:
    """  """

    _team: TeamSummary

    def to_dict(self) -> Dict[str, Any]:
        team = self._team.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "team": team,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        team = TeamSummary.from_dict(d.pop("team"))

        request_team_assignee = cls(
            team=team,
        )

        return request_team_assignee

    @property
    def team(self) -> TeamSummary:
        return self._team

    @team.setter
    def team(self, value: TeamSummary) -> None:
        self._team = value
