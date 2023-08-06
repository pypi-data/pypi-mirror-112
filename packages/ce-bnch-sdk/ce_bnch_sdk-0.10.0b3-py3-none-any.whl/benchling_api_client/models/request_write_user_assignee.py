from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="RequestWriteUserAssignee")


@attr.s(auto_attribs=True)
class RequestWriteUserAssignee:
    """  """

    _user_id: str

    def to_dict(self) -> Dict[str, Any]:
        user_id = self._user_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "userId": user_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_id = d.pop("userId")

        request_write_user_assignee = cls(
            user_id=user_id,
        )

        return request_write_user_assignee

    @property
    def user_id(self) -> str:
        return self._user_id

    @user_id.setter
    def user_id(self, value: str) -> None:
        self._user_id = value
