from baby_steps import given, then, when
from district42 import schema
from th import PathHolder

from valera import validate
from valera.errors import TypeValidationError


def test_none_validation():
    with when:
        result = validate(schema.none, None)

    with then:
        assert result.get_errors() == []


def test_none_validation_error():
    with given:
        value = False

    with when:
        result = validate(schema.none, value)

    with then:
        assert result.get_errors() == [TypeValidationError(PathHolder(), value, type(None))]
