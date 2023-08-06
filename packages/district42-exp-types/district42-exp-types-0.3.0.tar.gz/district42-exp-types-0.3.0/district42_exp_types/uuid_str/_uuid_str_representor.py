from typing import Any

from district42.representor import Representor
from niltype import Nil

from ._uuid_str_schema import UUIDStrSchema

__all__ = ("UUIDStrRepresentor",)


class UUIDStrRepresentor(Representor, extend=True):
    def visit_uuid_str(self, schema: UUIDStrSchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.uuid_str"

        if schema.props.value is not Nil:
            r += f"({schema.props.value!r})"

        return r
