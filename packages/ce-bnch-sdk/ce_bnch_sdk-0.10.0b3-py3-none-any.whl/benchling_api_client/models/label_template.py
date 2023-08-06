from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="LabelTemplate")


@attr.s(auto_attribs=True)
class LabelTemplate:
    """  """

    _id: str
    _name: str
    _zpl_template: str

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        name = self._name
        zpl_template = self._zpl_template

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "name": name,
                "zplTemplate": zpl_template,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        zpl_template = d.pop("zplTemplate")

        label_template = cls(
            id=id,
            name=name,
            zpl_template=zpl_template,
        )

        return label_template

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def zpl_template(self) -> str:
        return self._zpl_template

    @zpl_template.setter
    def zpl_template(self, value: str) -> None:
        self._zpl_template = value
