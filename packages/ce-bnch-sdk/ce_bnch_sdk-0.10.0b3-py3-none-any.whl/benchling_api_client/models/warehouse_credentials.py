from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="WarehouseCredentials")


@attr.s(auto_attribs=True)
class WarehouseCredentials:
    """  """

    _expires_at: str
    _password: str
    _username: str

    def to_dict(self) -> Dict[str, Any]:
        expires_at = self._expires_at
        password = self._password
        username = self._username

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "expiresAt": expires_at,
                "password": password,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expires_at = d.pop("expiresAt")

        password = d.pop("password")

        username = d.pop("username")

        warehouse_credentials = cls(
            expires_at=expires_at,
            password=password,
            username=username,
        )

        return warehouse_credentials

    @property
    def expires_at(self) -> str:
        return self._expires_at

    @expires_at.setter
    def expires_at(self, value: str) -> None:
        self._expires_at = value

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        self._password = value

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        self._username = value
