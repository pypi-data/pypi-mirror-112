from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="BlobUrl")


@attr.s(auto_attribs=True)
class BlobUrl:
    """  """

    _download_url: Union[Unset, str] = UNSET
    _expires_at: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        download_url = self._download_url
        expires_at = self._expires_at

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if download_url is not UNSET:
            field_dict["downloadURL"] = download_url
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        download_url = d.pop("downloadURL", UNSET)

        expires_at = d.pop("expiresAt", UNSET)

        blob_url = cls(
            download_url=download_url,
            expires_at=expires_at,
        )

        return blob_url

    @property
    def download_url(self) -> str:
        if isinstance(self._download_url, Unset):
            raise NotPresentError(self, "download_url")
        return self._download_url

    @download_url.setter
    def download_url(self, value: str) -> None:
        self._download_url = value

    @download_url.deleter
    def download_url(self) -> None:
        self._download_url = UNSET

    @property
    def expires_at(self) -> int:
        if isinstance(self._expires_at, Unset):
            raise NotPresentError(self, "expires_at")
        return self._expires_at

    @expires_at.setter
    def expires_at(self, value: int) -> None:
        self._expires_at = value

    @expires_at.deleter
    def expires_at(self) -> None:
        self._expires_at = UNSET
