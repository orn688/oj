from oj.lex import lex
from oj.tokens import Token, TokenType


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
