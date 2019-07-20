from oj.lex import lex, Token, TokenType


def test_lex_list():
    raw = "[true, false]"
    assert lex(raw) == [
        Token(TokenType.LEFT_BRACKET, "["),
        Token(TokenType.BOOLEAN, "true"),
        Token(TokenType.COMMA, ","),
        Token(TokenType.BOOLEAN, "false"),
        Token(TokenType.RIGHT_BRACKET, "]"),
    ]


def test_lex_nested_list():
    raw = "[true, [true, false]]"
    assert lex(raw) == [
        Token(TokenType.LEFT_BRACKET, "["),
        Token(TokenType.BOOLEAN, "true"),
        Token(TokenType.COMMA, ","),
        Token(TokenType.LEFT_BRACKET, "["),
        Token(TokenType.BOOLEAN, "true"),
        Token(TokenType.COMMA, ","),
        Token(TokenType.BOOLEAN, "false"),
        Token(TokenType.RIGHT_BRACKET, "]"),
        Token(TokenType.RIGHT_BRACKET, "]"),
    ]
