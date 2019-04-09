import re
from typing import Any, List, Optional, Tuple, Union

from oj.exceptions import ParseException
from oj.tokens import JSONLiteral, JSONSeparator, JSONToken

JSON_LEFT_BRACE = "{"
JSON_RIGHT_BRACE = "}"
JSON_LEFT_BRACKET = "["
JSON_RIGHT_BRACKET = "]"
JSON_COMMA = ","
JSON_COLON = ":"
JSON_SEPARATORS = [
    JSON_LEFT_BRACE,
    JSON_RIGHT_BRACE,
    JSON_LEFT_BRACKET,
    JSON_RIGHT_BRACKET,
    JSON_COMMA,
    JSON_COLON,
]
JSON_WHITESPACE = [" ", "\t", "\n", "\r", "\b"]
JSON_QUOTE = '"'
JSON_NAN = "NaN"
JSON_INFINITY = "Infinity"
JSON_TRUE = "true"
JSON_FALSE = "false"
JSON_NULL = "null"


def tokenize(string: str) -> List[JSONToken[Any]]:
    tokens: List[JSONToken[Any]] = []

    while string:
        if string[0].isspace():
            string = string[1:]
        for lex_method in (lex_string, lex_number, lex_bool, lex_null):
            token, string = lex_method(string)
            if token:
                tokens.append(token)
                break
        else:  # TODO: don't use for-else
            continue
        raise ParseException(f"Unexpected character: {string[0]}")

    return tokens


def lex_separator(string: str) -> Tuple[Optional[JSONSeparator], str]:
    if string[0] in JSON_SEPARATORS:
        return JSONSeparator(string[0]), string[1:]
    else:
        return None, string


def lex_string(string: str) -> Tuple[Optional[JSONLiteral[str]], str]:
    if string[0] != JSON_QUOTE:
        return None, string

    for i in range(1, len(string)):
        if string[i] == JSON_QUOTE:
            return JSONLiteral(string[1:i]), string[i + 1 :]

    raise ParseException("Unexpected end of string")


def lex_number(string: str) -> Tuple[Optional[JSONLiteral[Union[float, str]]], str]:
    number_regex = re.compile(
        rf"""
            (
                (?P<nan>{JSON_NAN})  # could be NaN (unsigned)
            |
                (?P<sign>\+|-)?
                (
                    (?P<inf>{JSON_INFINITY})  # could be infinity (signed)
                |
                    \d+(\.\d+)?  # at least one digit with optional decimal places
                    (e(\+|-)?\d+)?  # optional 'e' integer exponent
                )
            )
            (?=(\D|$))  # end of string or non-numeric character
        """,
        re.VERBOSE,
    )

    match = number_regex.match(string)
    if not match:
        return None, string

    num_string = match[0]
    sign = match.group("sign") or "+"
    if match.group("nan"):
        num = float("nan")
    elif match.group("inf"):
        num = float(sign + "inf")
    elif "." in num_string or "e" in num_string:
        num = float(num_string)
    else:
        num = int(num_string)

    return JSONLiteral(num), string[len(num_string) :]


def lex_bool(string: str) -> Tuple[Optional[JSONLiteral[bool]], str]:
    if string.startswith(JSON_TRUE):
        return JSONLiteral(True), string[len(JSON_TRUE) :]
    elif string.startswith(JSON_FALSE):
        return JSONLiteral(False), string[len(JSON_FALSE) :]

    return None, string


def lex_null(string: str) -> Tuple[Optional[JSONLiteral[None]], str]:
    if string.startswith(JSON_NULL):
        return JSONLiteral(None), string[len(JSON_NULL) :]

    return None, string
