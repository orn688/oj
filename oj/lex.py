from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional


class TokenType(Enum):
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    COMMA = auto()
    COLON = auto()
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()


class LexError(Exception):
    pass


@dataclass
class Token:
    token_type: TokenType
    lexeme: str


@dataclass
class TokenMatch:
    token: Token
    next_index: int


def lex(json_string: str) -> List[Token]:
    tokens: List[Token] = []
    index = 0

    while index < len(json_string):
        if json_string[index].isspace():
            index += 1
            continue
        for lex_func in [lex_delimiter, lex_bool]:
            match = lex_func(json_string, index)
            if match:
                tokens.append(match.token)
                index = match.next_index
                break
    return tokens


def lex_delimiter(json_string: str, index: int) -> Optional[TokenMatch]:
    delimiter_types = {
        "{": TokenType.LEFT_BRACE,
        "}": TokenType.RIGHT_BRACE,
        "[": TokenType.LEFT_BRACKET,
        "]": TokenType.RIGHT_BRACKET,
        ",": TokenType.COMMA,
        ":": TokenType.COLON,
    }
    lexeme = json_string[index]
    if lexeme not in delimiter_types:
        return None
    token = Token(delimiter_types[lexeme], lexeme)
    return TokenMatch(token=token, next_index=index + 1)


def lex_bool(json_string: str, index: int) -> Optional[TokenMatch]:
    for lexeme in "true", "false":
        if json_string.startswith(lexeme, index):
            token = Token(TokenType.BOOLEAN, lexeme)
            return TokenMatch(token=token, next_index=index + len(lexeme))
    return None
