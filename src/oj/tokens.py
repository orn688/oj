from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class JSONToken(Generic[T]):
    value: T


@dataclass
class JSONSeparator(JSONToken):
    """
    Comma, square bracket, curly brace, or colon
    """

    value: str


@dataclass
class JSONLiteral(JSONToken, Generic[T]):
    value: T
