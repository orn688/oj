from typing import IO, List, Any
from oj.lex import lex
from oj.parse import parse


def loads(json_string: str) -> List[Any]:
    tokens = lex(json_string)
    return parse(tokens)


def load(json_file: IO) -> List[bool]:
    return loads(json_file.read())
