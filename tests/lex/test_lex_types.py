from typing import Optional

import pytest
from hypothesis import given
from hypothesis import strategies as st

from oj.lex import LexFunc, lex_bool, lex_delimiter, lex_null, lex_string
from oj.tokens import TokenType


def assert_lexes_literal(
    lex_func: LexFunc,
    json_literal: str,
    expected_token_type: TokenType,
    expected_lexeme: Optional[str] = None,
) -> None:
    match = lex_func(json_literal, 0)
    assert match is not None
    assert match.next_index == len(json_literal)
    assert match.token.token_type == expected_token_type
    if expected_lexeme is None:
        # Assume that the lexeme is the entire input string unless the expected lexeme
        # is explicitly specified.
        expected_lexeme = json_literal
    assert match.token.lexeme == expected_lexeme


@pytest.mark.parametrize("bool_literal", ["true", "false"])
def test_lex_bool_positive(bool_literal):
    assert_lexes_literal(lex_bool, bool_literal, TokenType.BOOLEAN)


@given(st.from_regex(r"^(?!true|false)"))
def test_lex_bool_negative(json_string):
    match = lex_bool(json_string, 0)
    assert match is None


def test_lex_null_positive():
    assert_lexes_literal(lex_null, "null", TokenType.NULL)


@given(st.from_regex(r"^(?!null)"))
def test_lex_null_negative(json_string):
    assert_lexes_literal(lex_null, "null", TokenType.NULL)


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
