from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.user_validation_validation_status import UserValidationValidationStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserValidation")


@attr.s(auto_attribs=True)
class UserValidation:
    """  """

    _validation_comment: Union[Unset, str] = UNSET
    _validation_status: Union[Unset, UserValidationValidationStatus] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        validation_comment = self._validation_comment
        validation_status: Union[Unset, int] = UNSET
        if not isinstance(self._validation_status, Unset):
            validation_status = self._validation_status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if validation_comment is not UNSET:
            field_dict["validationComment"] = validation_comment
        if validation_status is not UNSET:
            field_dict["validationStatus"] = validation_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        validation_comment = d.pop("validationComment", UNSET)

        validation_status = None
        _validation_status = d.pop("validationStatus", UNSET)
        if _validation_status is not None and _validation_status is not UNSET:
            validation_status = UserValidationValidationStatus(_validation_status)

        user_validation = cls(
            validation_comment=validation_comment,
            validation_status=validation_status,
        )

        return user_validation

    @property
    def validation_comment(self) -> str:
        if isinstance(self._validation_comment, Unset):
            raise NotPresentError(self, "validation_comment")
        return self._validation_comment

    @validation_comment.setter
    def validation_comment(self, value: str) -> None:
        self._validation_comment = value

    @validation_comment.deleter
    def validation_comment(self) -> None:
        self._validation_comment = UNSET

    @property
    def validation_status(self) -> UserValidationValidationStatus:
        if isinstance(self._validation_status, Unset):
            raise NotPresentError(self, "validation_status")
        return self._validation_status

    @validation_status.setter
    def validation_status(self, value: UserValidationValidationStatus) -> None:
        self._validation_status = value

    @validation_status.deleter
    def validation_status(self) -> None:
        self._validation_status = UNSET
