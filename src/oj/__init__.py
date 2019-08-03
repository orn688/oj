from typing import IO, Union

from oj.exceptions import JSONDecodeError  # noqa: F401
from oj.lex import lex
from oj.parse import parse


def loads(json_string: str) -> Union[None, bool, float, str, list, dict]:
    tokens = lex(json_string)
    return parse(tokens)


def load(json_file: IO) -> Union[None, bool, float, str, list, dict]:
    return loads(json_file.read())
