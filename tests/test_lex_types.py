from typing import Optional

import pytest
from hypothesis import given
from hypothesis import strategies as st

from oj.lex import (
    LexFunc,
    lex,
    lex_bool,
    lex_delimiter,
    lex_null,
    lex_number,
    lex_string,
)
from oj.tokens import Token, TokenType


def assert_lexes_literal(
    lex_func: LexFunc,
    json_literal: str,
    expected_token_type: TokenType,
    expected_lexeme: Optional[str] = None,
) -> None:
    if expected_lexeme is None:
        # Assume that the lexeme is the entire input string unless the expected lexeme
        # is explicitly specified.
        expected_lexeme = json_literal
    match = lex_func(json_literal, 0)
    assert match is not None
    assert match.next_index == len(expected_lexeme)
    assert match.token.token_type == expected_token_type
    assert match.token.lexeme == expected_lexeme


@pytest.mark.parametrize("bool_literal", ["true", "false"])
def test_lex_bool_positive(bool_literal):
    assert_lexes_literal(lex_bool, bool_literal, TokenType.BOOLEAN)


def test_lex_null_positive():
    assert_lexes_literal(lex_null, "null", TokenType.NULL, "null")


delimiters = {
    "{": TokenType.OPEN_BRACE,
    "}": TokenType.CLOSE_BRACE,
    "[": TokenType.OPEN_BRACKET,
    "]": TokenType.CLOSE_BRACKET,
    ",": TokenType.COMMA,
    ":": TokenType.COLON,
}


@pytest.mark.parametrize("delimiter,expected_token_type", delimiters.items())
def test_lex_delimiter_positive(delimiter, expected_token_type):
    assert_lexes_literal(lex_delimiter, delimiter, expected_token_type)


@given(st.from_regex(r'"[^\\"]*"', fullmatch=True))
def test_lex_string_positive(string_literal):
    assert_lexes_literal(lex_string, string_literal, TokenType.STRING)


def test_lex_string_with_escapes():
    string_literal = r'"string with a \\ (backslash) and \" (quote)"'
    assert_lexes_literal(lex_string, string_literal, TokenType.STRING)


@pytest.mark.parametrize(
    "num", ["0", "5", "5.0", "0.0", "-0", "-1.0", "1e5", "1E5", "1E+5"]
)
def test_lex_number_positive(num):
    assert_lexes_literal(lex_number, num, TokenType.NUMBER)


def test_lex_list():
    raw = "[true, false, null]"
    assert lex(raw) == [
        Token(TokenType.OPEN_BRACKET, "[", 0),
        Token(TokenType.BOOLEAN, "true", 1),
        Token(TokenType.COMMA, ",", 5),
        Token(TokenType.BOOLEAN, "false", 7),
        Token(TokenType.COMMA, ",", 12),
        Token(TokenType.NULL, "null", 14),
        Token(TokenType.CLOSE_BRACKET, "]", 18),
    ]


def test_lex_nested_list():
    raw = "[true, [true, false]]"
    assert lex(raw) == [
        Token(TokenType.OPEN_BRACKET, "[", 0),
        Token(TokenType.BOOLEAN, "true", 1),
        Token(TokenType.COMMA, ",", 5),
        Token(TokenType.OPEN_BRACKET, "[", 7),
        Token(TokenType.BOOLEAN, "true", 8),
        Token(TokenType.COMMA, ",", 12),
        Token(TokenType.BOOLEAN, "false", 14),
        Token(TokenType.CLOSE_BRACKET, "]", 19),
        Token(TokenType.CLOSE_BRACKET, "]", 20),
    ]
