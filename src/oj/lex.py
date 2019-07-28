from dataclasses import dataclass
from typing import Callable, List, Optional

from oj.exceptions import InvalidJSON
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
    lex_funcs: List[LexFunc] = [
        lex_delimiter,
        lex_null,
        lex_bool,
        lex_nan,
        lex_infinity,  # Must come before lex_number, as both check for negative sign.
        lex_number,
        lex_string,
    ]

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
            raise InvalidJSON(f"invalid character at index {index}")
    return tokens


def lex_bool(json_string: str, start_index: int) -> Optional[TokenMatch]:
    for lexeme in "true", "false":
        if json_string.startswith(lexeme, start_index):
            token = Token(TokenType.BOOLEAN, lexeme, start_index)
            return TokenMatch(token=token, next_index=start_index + len(lexeme))
    return None


def lex_delimiter(json_string: str, start_index: int) -> Optional[TokenMatch]:
    delimiter_types = {
        "{": TokenType.OPEN_BRACE,
        "}": TokenType.CLOSE_BRACE,
        "[": TokenType.OPEN_BRACKET,
        "]": TokenType.CLOSE_BRACKET,
        ",": TokenType.COMMA,
        ":": TokenType.COLON,
    }
    lexeme = json_string[start_index]
    if lexeme not in delimiter_types:
        return None
    token = Token(delimiter_types[lexeme], lexeme, start_index)
    return TokenMatch(token=token, next_index=start_index + 1)


def lex_null(json_string: str, start_index: int) -> Optional[TokenMatch]:
    null_literal = "null"
    if json_string.startswith(null_literal, start_index):
        token = Token(TokenType.NULL, null_literal, start_index)
        return TokenMatch(token=token, next_index=start_index + len(null_literal))
    return None


def lex_nan(json_string: str, start_index: int) -> Optional[TokenMatch]:
    nan_literal = "NaN"
    if json_string.startswith(nan_literal, start_index):
        token = Token(TokenType.NAN, nan_literal, start_index)
        return TokenMatch(token=token, next_index=start_index + len(nan_literal))
    return None


def lex_infinity(json_string: str, start_index: int) -> Optional[TokenMatch]:
    inf_literal = "Infinity"
    negative_inf_literal = "-" + inf_literal
    for literal in (inf_literal, negative_inf_literal):
        if json_string.startswith(literal, start_index):
            token = Token(TokenType.INFINITY, literal, start_index)
            return TokenMatch(token=token, next_index=start_index + len(literal))
    return None


def lex_number(json_string: str, start_index: int) -> Optional[TokenMatch]:
    number_chars = {"-", "+", ".", "e", "E"} | set(map(str, range(10)))
    end_index = start_index
    while end_index < len(json_string) and json_string[end_index] in number_chars:
        end_index += 1
    if end_index == start_index:
        return None
    token = Token(TokenType.NUMBER, json_string[start_index:end_index], start_index)
    return TokenMatch(token=token, next_index=end_index)


def lex_string(json_string: str, start_index: int) -> Optional[TokenMatch]:
    if json_string[start_index] != '"':
        return None

    close_index = start_index + 1
    # Whether the previous character was a backslash preceded by an even number of
    # backslashes.
    escaped = False
    for close_index in range(start_index + 1, len(json_string)):
        char = json_string[close_index]
        if not escaped and char == "\\":
            escaped = True
        elif escaped:
            escaped = False
        elif char == '"':
            string = json_string[start_index : close_index + 1]
            token = Token(TokenType.STRING, string, start_index)
            return TokenMatch(token=token, next_index=close_index + 1)

    # Got to the end of the input string without finding a closing quote.
    raise InvalidJSON(f"unterminated string starting at index {start_index}")
