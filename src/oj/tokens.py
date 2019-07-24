from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    OPEN_BRACE = auto()
    CLOSE_BRACE = auto()
    OPEN_BRACKET = auto()
    CLOSE_BRACKET = auto()
    COMMA = auto()
    COLON = auto()
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    NULL = auto()


@dataclass
class Token:
    token_type: TokenType
    lexeme: str
    index: int
