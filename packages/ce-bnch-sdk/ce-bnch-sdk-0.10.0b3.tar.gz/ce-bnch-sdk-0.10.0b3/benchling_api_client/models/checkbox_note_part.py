from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.checkbox_note_part_type import CheckboxNotePartType
from ..models.entry_link import EntryLink
from ..types import UNSET, Unset

T = TypeVar("T", bound="CheckboxNotePart")


@attr.s(auto_attribs=True)
class CheckboxNotePart:
    """ One "line" of a checklist """

    _checked: Union[Unset, bool] = UNSET
    _links: Union[Unset, List[EntryLink]] = UNSET
    _text: Union[Unset, str] = UNSET
    _type: Union[Unset, CheckboxNotePartType] = UNSET
    _indentation: Union[Unset, int] = 0

    def to_dict(self) -> Dict[str, Any]:
        checked = self._checked
        links: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._links, Unset):
            links = []
            for links_item_data in self._links:
                links_item = links_item_data.to_dict()

                links.append(links_item)

        text = self._text
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        indentation = self._indentation

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if checked is not UNSET:
            field_dict["checked"] = checked
        if links is not UNSET:
            field_dict["links"] = links
        if text is not UNSET:
            field_dict["text"] = text
        if type is not UNSET:
            field_dict["type"] = type
        if indentation is not UNSET:
            field_dict["indentation"] = indentation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        checked = d.pop("checked", UNSET)

        links = []
        _links = d.pop("links", UNSET)
        for links_item_data in _links or []:
            links_item = EntryLink.from_dict(links_item_data)

            links.append(links_item)

        text = d.pop("text", UNSET)

        type = None
        _type = d.pop("type", UNSET)
        if _type is not None and _type is not UNSET:
            type = CheckboxNotePartType(_type)

        indentation = d.pop("indentation", UNSET)

        checkbox_note_part = cls(
            checked=checked,
            links=links,
            text=text,
            type=type,
            indentation=indentation,
        )

        return checkbox_note_part

    @property
    def checked(self) -> bool:
        if isinstance(self._checked, Unset):
            raise NotPresentError(self, "checked")
        return self._checked

    @checked.setter
    def checked(self, value: bool) -> None:
        self._checked = value

    @checked.deleter
    def checked(self) -> None:
        self._checked = UNSET

    @property
    def links(self) -> List[EntryLink]:
        if isinstance(self._links, Unset):
            raise NotPresentError(self, "links")
        return self._links

    @links.setter
    def links(self, value: List[EntryLink]) -> None:
        self._links = value

    @links.deleter
    def links(self) -> None:
        self._links = UNSET

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

    @property
    def type(self) -> CheckboxNotePartType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: CheckboxNotePartType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

    @property
    def indentation(self) -> int:
        if isinstance(self._indentation, Unset):
            raise NotPresentError(self, "indentation")
        return self._indentation

    @indentation.setter
    def indentation(self, value: int) -> None:
        self._indentation = value

    @indentation.deleter
    def indentation(self) -> None:
        self._indentation = UNSET
