from typing import Any
from uuid import uuid4

from blahblah import Generator
from niltype import Nil

from ._uuid_str_schema import UUIDStrSchema

__all__ = ("UUIDStrGenerator",)


class UUIDStrGenerator(Generator, extend=True):
    def visit_uuid_str(self, schema: UUIDStrSchema, **kwargs: Any) -> str:
        if schema.props.value is not Nil:
            return schema.props.value
        return str(uuid4())
