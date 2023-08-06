from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.dna_alignment_base_algorithm import DnaAlignmentBaseAlgorithm
from ..models.dna_alignment_base_files_item import DnaAlignmentBaseFilesItem
from ..models.dna_template_alignment_file import DnaTemplateAlignmentFile
from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaAlignmentBase")


@attr.s(auto_attribs=True)
class DnaAlignmentBase:
    """  """

    _algorithm: DnaAlignmentBaseAlgorithm
    _files: List[Union[DnaAlignmentBaseFilesItem, DnaTemplateAlignmentFile]]
    _name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        algorithm = self._algorithm.value

        files = []
        for files_item_data in self._files:
            if isinstance(files_item_data, DnaAlignmentBaseFilesItem):
                files_item = files_item_data.to_dict()

            else:
                files_item = files_item_data.to_dict()

            files.append(files_item)

        name = self._name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "algorithm": algorithm,
                "files": files,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        algorithm = DnaAlignmentBaseAlgorithm(d.pop("algorithm"))

        files = []
        _files = d.pop("files")
        for files_item_data in _files:

            def _parse_files_item(
                data: Union[Dict[str, Any]]
            ) -> Union[DnaAlignmentBaseFilesItem, DnaTemplateAlignmentFile]:
                files_item: Union[DnaAlignmentBaseFilesItem, DnaTemplateAlignmentFile]
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    files_item = DnaAlignmentBaseFilesItem.from_dict(data)

                    return files_item
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                files_item = DnaTemplateAlignmentFile.from_dict(data)

                return files_item

            files_item = _parse_files_item(files_item_data)

            files.append(files_item)

        name = d.pop("name", UNSET)

        dna_alignment_base = cls(
            algorithm=algorithm,
            files=files,
            name=name,
        )

        return dna_alignment_base

    @property
    def algorithm(self) -> DnaAlignmentBaseAlgorithm:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value: DnaAlignmentBaseAlgorithm) -> None:
        self._algorithm = value

    @property
    def files(self) -> List[Union[DnaAlignmentBaseFilesItem, DnaTemplateAlignmentFile]]:
        return self._files

    @files.setter
    def files(self, value: List[Union[DnaAlignmentBaseFilesItem, DnaTemplateAlignmentFile]]) -> None:
        self._files = value

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET
