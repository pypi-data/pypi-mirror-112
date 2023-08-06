from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.entry_link import EntryLink
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryTableCell")


@attr.s(auto_attribs=True)
class EntryTableCell:
    """  """

    _link: Union[Unset, EntryLink] = UNSET
    _text: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        link: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._link, Unset):
            link = self._link.to_dict()

        text = self._text

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if link is not UNSET:
            field_dict["link"] = link
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        link: Union[Unset, EntryLink] = UNSET
        _link = d.pop("link", UNSET)
        if not isinstance(_link, Unset):
            link = EntryLink.from_dict(_link)

        text = d.pop("text", UNSET)

        entry_table_cell = cls(
            link=link,
            text=text,
        )

        return entry_table_cell

    @property
    def link(self) -> EntryLink:
        if isinstance(self._link, Unset):
            raise NotPresentError(self, "link")
        return self._link

    @link.setter
    def link(self, value: EntryLink) -> None:
        self._link = value

    @link.deleter
    def link(self) -> None:
        self._link = UNSET

    @property
    def text(self) -> str:
        if isinstance(self._text, Unset):
            raise NotPresentError(self, "text")
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

    @text.deleter
    def text(self) -> None:
        self._text = UNSET
