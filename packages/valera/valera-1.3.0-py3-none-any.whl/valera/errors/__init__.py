from abc import ABC
from typing import Any, Tuple, Type

from district42 import GenericSchema
from th import PathHolder

__all__ = ("ValidationError", "TypeValidationError", "ValueValidationError",
           "MinValueValidationError", "MaxValueValidationError", "LengthValidationError",
           "MinLengthValidationError", "MaxLengthValidationError", "AlphabetValidationError",
           "IndexValidationError", "ExtraElementValidationError", "MissingKeyValidationError",
           "ExtraKeyValidationError", "SchemaMismatchValidationError", "SubstrValidationError",
           "RegexValidationError",)


class ValidationError(ABC):
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class TypeValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, expected_type: Type[Any]) -> None:
        self._path = path
        self._actual_value = actual_value
        self._expected_type = expected_type

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self._path!r}, {self._actual_value!r}, "
                f"{self._expected_type!r})")


class ValueValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, expected_value: Any) -> None:
        self._path = path
        self._actual_value = actual_value
        self._expected_value = expected_value

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self._path!r}, {self._actual_value!r}, "
                f"{self._expected_value!r})")


class MinValueValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, min_value: Any) -> None:
        self._path = path
        self._actual_value = actual_value
        self._min_value = min_value

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self._path!r}, {self._actual_value!r}, "
                f"{self._min_value!r})")


class MaxValueValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, max_value: Any) -> None:
        self._path = path
        self._actual_value = actual_value
        self._max_value = max_value

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self._path!r}, {self._actual_value!r}, "
                f"{self._max_value!r})")


class LengthValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, length: int) -> None:
        self._path = path
        self._actual_value = actual_value
        self._length = length

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self._path!r}, {self._actual_value!r}, "
                f"{self._length!r})")


class MinLengthValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, min_length: int) -> None:
        self._path = path
        self._actual_value = actual_value
        self._min_length = min_length

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self._path!r}, {self._actual_value!r}, "
                f"{self._min_length!r})")


class MaxLengthValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, max_length: int) -> None:
        self._path = path
        self._actual_value = actual_value
        self._max_length = max_length

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self._path!r}, {self._actual_value!r}, "
                f"{self._max_length!r})")


class AlphabetValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: str, alphabet: str) -> None:
        self._path = path
        self._actual_value = actual_value
        self._alphabet = alphabet

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self._path!r}, {self._actual_value!r}, "
                f"{self._alphabet!r})")


class IndexValidationError(ValidationError):
    def __init__(self, path: PathHolder, index: int) -> None:
        self._path = path
        self._index = index

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._path!r}, {self._index!r})"


class ExtraElementValidationError(ValidationError):
    def __init__(self, path: PathHolder, index: int) -> None:
        self._path = path
        self._index = index

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._path!r}, {self._index!r})"


class MissingKeyValidationError(ValidationError):
    def __init__(self, path: PathHolder, key: Any) -> None:
        self._path = path
        self._missing_key = key

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._path!r}, {self._missing_key!r})"


class ExtraKeyValidationError(ValidationError):
    def __init__(self, path: PathHolder, key: Any) -> None:
        self._path = path
        self._extra_key = key

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._path!r}, {self._extra_key!r})"


class SchemaMismatchValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any,
                 expected_schemas: Tuple[GenericSchema, ...]) -> None:
        self._path = path
        self._actual_value = actual_value
        self._expected_schemas = expected_schemas

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self._path!r}, {self._actual_value!r}, "
                f"{self._expected_schemas!r})")


class SubstrValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, substr: str) -> None:
        self._path = path
        self._actual_value = actual_value
        self._substr = substr

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self._path!r}, {self._actual_value!r}, "
                f"{self._substr!r})")


class RegexValidationError(ValidationError):
    def __init__(self, path: PathHolder, actual_value: Any, pattern: str) -> None:
        self._path = path
        self._actual_value = actual_value
        self._pattern = pattern

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self._path!r}, {self._actual_value!r}, "
                f"{self._pattern!r})")
