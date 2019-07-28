import pytest
from hypothesis import given
from hypothesis import strategies as st

from oj.parse import parse_string
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
