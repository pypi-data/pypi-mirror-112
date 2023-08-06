from typing import Any

from district42 import GenericSchema
from district42.types import Schema

from ._validation_result import ValidationResult
from ._validator import Validator
from ._version import version

__version__ = version
__all__ = ("validate", "Validator", "ValidationResult",)


_validator = Validator()


def validate(schema: GenericSchema, value: Any, **kwargs: Any) -> ValidationResult:
    return schema.__accept__(_validator, value=value, **kwargs)


def eq(schema: GenericSchema, value: Any) -> bool:
    if isinstance(value, Schema):
        return isinstance(value, schema.__class__) and (schema.props == value.props)
    return not validate(schema, value=value).has_errors()


Schema.__override__(Schema.__eq__.__name__, eq)
