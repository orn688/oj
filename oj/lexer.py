import re

import attr

from .exceptions import ParseException

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
JSON_WHITESPACE = [" ", "\n", "\t"]
JSON_QUOTE = '"'
JSON_NAN = "NaN"
JSON_INFINITY = "Infinity"
JSON_TRUE = "true"
JSON_FALSE = "false"
JSON_NULL = "null"


class JSONToken:
    pass


@attr.s
class JSONString(JSONToken):
    value = attr.ib()


@attr.s
class JSONNull(JSONToken):
    pass


def lex(string):
    tokens = []

    while string:
        json_string, string = lex_string(string)
        if json_string is not None:
            tokens.append(json_string)
            continue

        json_number, string = lex_number(string)
        if json_number is not None:
            tokens.append(json_number)
            continue

        json_bool, string = lex_bool(string)
        if json_bool is not None:
            tokens.append(json_bool)
            continue

        json_null, string = lex_null(string)
        if json_null is not None:
            tokens.append(json_null)

        if string[0] in JSON_WHITESPACE:
            string = string[1:]
        elif string[0] in JSON_SEPARATORS:
            print(string[0])
            tokens.append(string[0])
            string = string[1:]
        else:
            raise ParseException(f"Unexpected character: {string[0]}")

    return tokens


def lex_string(string):
    if string[0] == JSON_QUOTE:
        string = string[1:]
    else:
        return None, string

    for i, char in enumerate(string):
        if char == JSON_QUOTE:
            return JSONString(string[:i]), string[i + 1 :]

    raise ParseException("Unexpected end of string")


def lex_number(string):
    number_regex = re.compile(
        rf"""
            (
                (?P<nan>{JSON_NAN})  # could be NaN (unsigned)
            |
                (?P<sign>\+|-)?
                (
                    (?P<inf>{JSON_INFINITY})  # could be infinity (signed)
                |
                    (
                        \d+(\.\d*)?  # at least one digit with optional decimal places
                    |
                        \d*\.\d+  # zero or more digits with at least one decimal place
                    )
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

    return num, string[len(num_string) :]


def lex_bool(string):
    if string.startswith(JSON_TRUE):
        return True, string[len(JSON_TRUE) :]
    elif string.startswith(JSON_FALSE):
        return False, string[len(JSON_FALSE) :]

    return None, string


def lex_null(string):
    if string.startswith(JSON_NULL):
        return JSONNull(), string[len(JSON_NULL) :]

    return None, string
