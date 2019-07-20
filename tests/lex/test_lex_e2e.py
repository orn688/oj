from oj.lex import lex
from oj.tokens import Token, TokenType


def test_lex_list():
    raw = "[true, false, null]"
    assert lex(raw) == [
        Token(TokenType.OPEN_BRACKET, "["),
        Token(TokenType.BOOLEAN, "true"),
        Token(TokenType.COMMA, ","),
        Token(TokenType.BOOLEAN, "false"),
        Token(TokenType.COMMA, ","),
        Token(TokenType.NULL, "null"),
        Token(TokenType.CLOSE_BRACKET, "]"),
    ]


def test_lex_nested_list():
    raw = "[true, [true, false]]"
    assert lex(raw) == [
        Token(TokenType.OPEN_BRACKET, "["),
        Token(TokenType.BOOLEAN, "true"),
        Token(TokenType.COMMA, ","),
        Token(TokenType.OPEN_BRACKET, "["),
        Token(TokenType.BOOLEAN, "true"),
        Token(TokenType.COMMA, ","),
        Token(TokenType.BOOLEAN, "false"),
        Token(TokenType.CLOSE_BRACKET, "]"),
        Token(TokenType.CLOSE_BRACKET, "]"),
    ]
