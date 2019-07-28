import pytest
from hypothesis import given
from hypothesis import strategies as st

from oj.exceptions import InvalidJSON
from oj.parse import parse_string, parse_number
from oj.tokens import Token, TokenType


@pytest.mark.parametrize(
    "escaped_char,result_char",
    {
        '"': '"',
        "\\": "\\",
        "/": "/",
        "b": "\b",
        "f": "\f",
        "n": "\n",
        "r": "\r",
        "t": "\t",
    }.items(),
)
def test_parse_escape_chars(escaped_char, result_char):
    lexeme = f'"\\{escaped_char}"'
    token = Token(TokenType.STRING, lexeme, 0)
    assert parse_string(token) == result_char


@given(st.integers(0, 16 ** 4 - 1))
def test_parse_hex(char_point):
    hex_point = hex(char_point)[2:].zfill(4)
    lexeme = f'"\\u{hex_point}"'
    token = Token(TokenType.STRING, lexeme, 0)
    assert parse_string(token) == chr(char_point)


@given(st.integers())
def test_parse_number_integer(num):
    token = Token(TokenType.NUMBER, str(num), 0)
    assert parse_number(token) == num


@given(st.floats(-100, 100))
def test_parse_number_float(num):
    token = Token(TokenType.NUMBER, str(num), 0)
    assert pytest.approx(parse_number(token), num, abs=1e-20)


def test_parse_number_rejects_leading_zeros():
    token = Token(TokenType.NUMBER, "05", 0)
    with pytest.raises(InvalidJSON):
        parse_number(token)


# Limit the size of floats so that str(base) doesn't return a string in scientific
# notation.
# Limit the size of the exponent so that base * 10**exponent doesn't overflow.
@given(base=st.floats(-100, 100), exponent=st.integers(-20, 20))
def test_parse_number_scientific_notations(base, exponent):
    token = Token(TokenType.NUMBER, f'{base}e{exponent}', 0)
    expected = float(base) * (10.0 ** exponent)
    assert pytest.approx(parse_number(token), expected, abs=1e-20)
