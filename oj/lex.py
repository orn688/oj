from dataclasses import dataclass
from typing import Callable, List, Optional

from oj.exceptions import LexError
from oj.tokens import Token, TokenType


@dataclass
class TokenMatch:
    token: Token
    next_index: int


LexFunc = Callable[[str, int], Optional[TokenMatch]]


def lex(json_string: str) -> List[Token]:
    # Ordering of lex functions is based roughly on efficiency of the function
    # (faster functions first) and how common the corresponding token type is
    # expected to be (more common first) to avoid expensive negative checks.
    lex_funcs: List[LexFunc] = [lex_delimiter, lex_bool, lex_null]

    tokens: List[Token] = []
    index = 0
    while index < len(json_string):
        if json_string[index].isspace():
            index += 1
            continue
        for lex_func in lex_funcs:
            match = lex_func(json_string, index)
            if match:
                tokens.append(match.token)
                index = match.next_index
                break
    return tokens


def lex_bool(json_string: str, index: int) -> Optional[TokenMatch]:
    for lexeme in "true", "false":
        if json_string.startswith(lexeme, index):
            token = Token(TokenType.BOOLEAN, lexeme)
            return TokenMatch(token=token, next_index=index + len(lexeme))
    return None


def lex_delimiter(json_string: str, index: int) -> Optional[TokenMatch]:
    delimiter_types = {
        "{": TokenType.OPEN_BRACE,
        "}": TokenType.CLOSE_BRACE,
        "[": TokenType.OPEN_BRACKET,
        "]": TokenType.CLOSE_BRACKET,
        ",": TokenType.COMMA,
        ":": TokenType.COLON,
    }
    lexeme = json_string[index]
    if lexeme not in delimiter_types:
        return None
    token = Token(delimiter_types[lexeme], lexeme)
    return TokenMatch(token=token, next_index=index + 1)


def lex_null(json_string: str, index: int) -> Optional[TokenMatch]:
    null_literal = "null"
    if json_string.startswith(null_literal, index):
        token = Token(TokenType.NULL, null_literal)
        return TokenMatch(token=token, next_index=index + len(null_literal))
    return None


def lex_string(json_string: str, index: int) -> Optional[TokenMatch]:
    quote = '"'
    if json_string[index] != quote:
        return None
    close_index = index + 1
    escaped = False  # If the last character was a backslash.
    while close_index < len(json_string):
        if escaped:
            escaped = False
            continue

        char = json_string[close_index]
        if char == "\\":
            escaped = True
        elif char == quote:
            lexeme = json_string[index : close_index + 1]
            token = Token(TokenType.STRING, lexeme)
            return TokenMatch(token=token, next_index=close_index + 1)

    raise LexError("unterminated string")
