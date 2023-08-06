from typing import Any
from uuid import UUID

from niltype import Nil, Nilable
from th import PathHolder
from valera import ValidationResult, Validator
from valera.errors import ValueValidationError

from ._uuid_str_schema import UUIDStrSchema

__all__ = ("UUIDStrValidator",)


class UUIDStrValidator(Validator, extend=True):
    def visit_uuid_str(self, schema: UUIDStrSchema, *,
                       value: Any = Nil, path: Nilable[PathHolder] = Nil,
                       **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, str):
            return result.add_error(error)

        try:
            actual_value = UUID(value)
        except (TypeError, ValueError):
            error = ValueValidationError(path, value, schema.props.value)
            return result.add_error(error)

        if schema.props.value is not Nil:
            if actual_value != UUID(schema.props.value):
                error = ValueValidationError(path, value, schema.props.value)
                return result.add_error(error)

        return result
