import pytest
from oj.tokens import Token, TokenType
from oj.parse import parse_string


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


def test_parse_hex():
    json_string = '"'
