from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.assay_run_note_part import AssayRunNotePart
from ..models.checkbox_note_part import CheckboxNotePart
from ..models.external_file_note_part import ExternalFileNotePart
from ..models.simple_note_part import SimpleNotePart
from ..models.table_note_part import TableNotePart
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryDay")


@attr.s(auto_attribs=True)
class EntryDay:
    """  """

    _date: Union[Unset, str] = UNSET
    _notes: Union[
        Unset,
        List[Union[SimpleNotePart, TableNotePart, CheckboxNotePart, ExternalFileNotePart, AssayRunNotePart]],
    ] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        date = self._date
        notes: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._notes, Unset):
            notes = []
            for notes_item_data in self._notes:
                if isinstance(notes_item_data, SimpleNotePart):
                    notes_item = notes_item_data.to_dict()

                elif isinstance(notes_item_data, TableNotePart):
                    notes_item = notes_item_data.to_dict()

                elif isinstance(notes_item_data, CheckboxNotePart):
                    notes_item = notes_item_data.to_dict()

                elif isinstance(notes_item_data, ExternalFileNotePart):
                    notes_item = notes_item_data.to_dict()

                else:
                    notes_item = notes_item_data.to_dict()

                notes.append(notes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if date is not UNSET:
            field_dict["date"] = date
        if notes is not UNSET:
            field_dict["notes"] = notes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        date = d.pop("date", UNSET)

        notes = []
        _notes = d.pop("notes", UNSET)
        for notes_item_data in _notes or []:

            def _parse_notes_item(
                data: Union[Dict[str, Any]]
            ) -> Union[
                SimpleNotePart, TableNotePart, CheckboxNotePart, ExternalFileNotePart, AssayRunNotePart
            ]:
                notes_item: Union[
                    SimpleNotePart, TableNotePart, CheckboxNotePart, ExternalFileNotePart, AssayRunNotePart
                ]
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    notes_item = SimpleNotePart.from_dict(data)

                    return notes_item
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    notes_item = TableNotePart.from_dict(data)

                    return notes_item
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    notes_item = CheckboxNotePart.from_dict(data)

                    return notes_item
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    notes_item = ExternalFileNotePart.from_dict(data)

                    return notes_item
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                notes_item = AssayRunNotePart.from_dict(data)

                return notes_item

            notes_item = _parse_notes_item(notes_item_data)

            notes.append(notes_item)

        entry_day = cls(
            date=date,
            notes=notes,
        )

        return entry_day

    @property
    def date(self) -> str:
        if isinstance(self._date, Unset):
            raise NotPresentError(self, "date")
        return self._date

    @date.setter
    def date(self, value: str) -> None:
        self._date = value

    @date.deleter
    def date(self) -> None:
        self._date = UNSET

    @property
    def notes(
        self,
    ) -> List[Union[SimpleNotePart, TableNotePart, CheckboxNotePart, ExternalFileNotePart, AssayRunNotePart]]:
        if isinstance(self._notes, Unset):
            raise NotPresentError(self, "notes")
        return self._notes

    @notes.setter
    def notes(
        self,
        value: List[
            Union[SimpleNotePart, TableNotePart, CheckboxNotePart, ExternalFileNotePart, AssayRunNotePart]
        ],
    ) -> None:
        self._notes = value

    @notes.deleter
    def notes(self) -> None:
        self._notes = UNSET
