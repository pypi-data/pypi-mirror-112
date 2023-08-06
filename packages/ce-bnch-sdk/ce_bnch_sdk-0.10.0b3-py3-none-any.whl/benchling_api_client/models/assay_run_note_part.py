from typing import Any, Dict, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.assay_run_note_part_type import AssayRunNotePartType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayRunNotePart")


@attr.s(auto_attribs=True)
class AssayRunNotePart:
    """  """

    _assay_run_id: Union[Unset, None, str] = UNSET
    _assay_run_schema_id: Union[Unset, str] = UNSET
    _type: Union[Unset, AssayRunNotePartType] = UNSET
    _indentation: Union[Unset, int] = 0

    def to_dict(self) -> Dict[str, Any]:
        assay_run_id = self._assay_run_id
        assay_run_schema_id = self._assay_run_schema_id
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        indentation = self._indentation

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if assay_run_id is not UNSET:
            field_dict["assayRunId"] = assay_run_id
        if assay_run_schema_id is not UNSET:
            field_dict["assayRunSchemaId"] = assay_run_schema_id
        if type is not UNSET:
            field_dict["type"] = type
        if indentation is not UNSET:
            field_dict["indentation"] = indentation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assay_run_id = d.pop("assayRunId", UNSET)

        assay_run_schema_id = d.pop("assayRunSchemaId", UNSET)

        type = None
        _type = d.pop("type", UNSET)
        if _type is not None and _type is not UNSET:
            type = AssayRunNotePartType(_type)

        indentation = d.pop("indentation", UNSET)

        assay_run_note_part = cls(
            assay_run_id=assay_run_id,
            assay_run_schema_id=assay_run_schema_id,
            type=type,
            indentation=indentation,
        )

        return assay_run_note_part

    @property
    def assay_run_id(self) -> Optional[str]:
        if isinstance(self._assay_run_id, Unset):
            raise NotPresentError(self, "assay_run_id")
        return self._assay_run_id

    @assay_run_id.setter
    def assay_run_id(self, value: Optional[str]) -> None:
        self._assay_run_id = value

    @assay_run_id.deleter
    def assay_run_id(self) -> None:
        self._assay_run_id = UNSET

    @property
    def assay_run_schema_id(self) -> str:
        if isinstance(self._assay_run_schema_id, Unset):
            raise NotPresentError(self, "assay_run_schema_id")
        return self._assay_run_schema_id

    @assay_run_schema_id.setter
    def assay_run_schema_id(self, value: str) -> None:
        self._assay_run_schema_id = value

    @assay_run_schema_id.deleter
    def assay_run_schema_id(self) -> None:
        self._assay_run_schema_id = UNSET

    @property
    def type(self) -> AssayRunNotePartType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: AssayRunNotePartType) -> None:
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
