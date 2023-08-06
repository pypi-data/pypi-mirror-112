from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="AsyncTaskLink")


@attr.s(auto_attribs=True)
class AsyncTaskLink:
    """  """

    _task_id: str

    def to_dict(self) -> Dict[str, Any]:
        task_id = self._task_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "taskId": task_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        task_id = d.pop("taskId")

        async_task_link = cls(
            task_id=task_id,
        )

        return async_task_link

    @property
    def task_id(self) -> str:
        return self._task_id

    @task_id.setter
    def task_id(self, value: str) -> None:
        self._task_id = value
