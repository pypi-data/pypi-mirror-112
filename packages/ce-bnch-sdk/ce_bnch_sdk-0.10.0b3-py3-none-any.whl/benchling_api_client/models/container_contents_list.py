from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.container_content import ContainerContent

T = TypeVar("T", bound="ContainerContentsList")


@attr.s(auto_attribs=True)
class ContainerContentsList:
    """  """

    _contents: List[ContainerContent]

    def to_dict(self) -> Dict[str, Any]:
        contents = []
        for contents_item_data in self._contents:
            contents_item = contents_item_data.to_dict()

            contents.append(contents_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "contents": contents,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        contents = []
        _contents = d.pop("contents")
        for contents_item_data in _contents:
            contents_item = ContainerContent.from_dict(contents_item_data)

            contents.append(contents_item)

        container_contents_list = cls(
            contents=contents,
        )

        return container_contents_list

    @property
    def contents(self) -> List[ContainerContent]:
        return self._contents

    @contents.setter
    def contents(self, value: List[ContainerContent]) -> None:
        self._contents = value
