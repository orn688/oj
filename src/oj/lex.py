import re
from dataclasses import dataclass
from typing import Callable, List, Match, Optional

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
    lex_funcs: List[LexFunc] = [lex_delimiter, lex_null, lex_bool, lex_string]

    tokens: List[Token] = []
    index = 0
    while index < len(json_string):
        if json_string[index].isspace():
            index += 1
            continue
        match: Optional[TokenMatch]
        for lex_func in lex_funcs:
            match = lex_func(json_string, index)
            if match:
                tokens.append(match.token)
                index = match.next_index
                break
        if not match:
            raise LexError(f"invalid character at index {index}")
    return tokens


def lex_bool(json_string: str, index: int) -> Optional[TokenMatch]:
    for lexeme in "true", "false":
        if json_string.startswith(lexeme, index):
            token = Token(TokenType.BOOLEAN, lexeme, index)
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
    token = Token(delimiter_types[lexeme], lexeme, index)
    return TokenMatch(token=token, next_index=index + 1)


def lex_null(json_string: str, index: int) -> Optional[TokenMatch]:
    null_literal = "null"
    if json_string.startswith(null_literal, index):
        token = Token(TokenType.NULL, null_literal, index)
        return TokenMatch(token=token, next_index=index + len(null_literal))
    return None


def lex_string(json_string: str, index: int) -> Optional[TokenMatch]:
    quote = '"'
    backslash = "\\"
    if json_string[index] != quote:
        return None

    close_index = index + 1
    escaped = False  # If the last character was a backslash.
    chars: List[str] = []
    for close_index in range(index + 1, len(json_string)):
        char = json_string[close_index]
        if not escaped and char == backslash:
            escaped = True
        elif not escaped and char == quote:
            string = python_unicode("".join(chars))
            token = Token(TokenType.STRING, string, index)
            return TokenMatch(token=token, next_index=close_index + 1)
        else:
            if escaped:
                escaped = False
                char = {
                    "b": "\b",
                    "f": "\f",
                    "n": "\n",
                    "r": "\r",
                    "t": "\t",
                    # For unicode literals (starting with "\u"), leave the preceding
                    # backslash to be searched and replaced later.
                    "u": "\\u",
                }.get(char, char)
            chars.append(char)

    # Got to the end of the input string without finding a closing quote.
    raise LexError(f"unterminated string starting at index {index}")


def python_unicode(json_string: str) -> str:
    def replace_func(match: Match[str]) -> str:
        char_point_digits = match.group("hex").lstrip("\\u")
        char_point = int(char_point_digits, base=16)
        return chr(char_point)

    return re.sub(r"(?P<hex>\\u[\da-f]{4})", replace_func, json_string)
