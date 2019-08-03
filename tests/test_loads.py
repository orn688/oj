import pytest
from hypothesis import given
from hypothesis import strategies as st

import oj
from oj.exceptions import InvalidJSON


@pytest.mark.parametrize("boolean", [True, False])
def test_bool_positive(boolean):
    literal = str(boolean).lower()
    assert oj.loads(literal) == boolean


def test_null_positive():
    assert oj.loads("null") is None


def test_empty_string():
    assert oj.loads('""') == ""


@given(st.from_regex(r'"[^\\"]*"', fullmatch=True))
def test_string_positive(string_literal):
    assert oj.loads(string_literal) == string_literal[1:-1]


def test_string_with_escapes():
    string_literal = r'"string with a \\ (backslash) and \" (quote)"'
    assert oj.loads(string_literal) == r'string with a \ (backslash) and " (quote)'


@pytest.mark.parametrize("num", ["0", "5", "-0", "-5", "12313", "-12313"])
def test_integer_positive(num):
    assert oj.loads(num) == int(num)


@pytest.mark.parametrize("num", ["5.0", "0.0", "-1.0", "1e5", "1E5", "1E+5"])
def test_float_positive(num):
    assert oj.loads(num) == float(num)


def test_list():
    lst = "[true, false, null]"
    assert oj.loads(lst) == [True, False, None]


def test_lex_nested_list():
    lst = "[true, [false, null]]"
    assert oj.loads(lst) == [True, [False, None]]


def test_loads_empty_list():
    assert oj.loads("[]") == []


def test_loads_list():
    assert oj.loads("[true, 0.5, null]") == [True, 0.5, None]


def test_loads_nested_list():
    assert oj.loads('[true, [1, "string"]]') == [True, [1, "string"]]


def test_loads_empty_object():
    assert oj.loads("{}") == {}


def test_loads_object():
    assert oj.loads('{"key1": 1, "key2": "val"}') == {"key1": 1, "key2": "val"}


def test_rejects_non_string_keys():
    with pytest.raises(InvalidJSON):
        assert oj.loads('{5: "val"}')
