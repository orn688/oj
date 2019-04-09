from typing import Any, List

from oj import lex, tokens as t


def parse(tokens: List[t.JSONToken[Any]]):
    if isinstance(tokens[0], t.JSONSeparator):
        if tokens[0].value == lex.JSON_LEFT_BRACKET:
            return parse_array(tokens[1:])
        elif tokens[0] == lex.JSON_LEFT_BRACE:
            return parse_object(tokens[1:])
    else:
        return tokens[0], tokens[1:]


def parse_array(tokens):
    array = []

    while tokens and tokens[0] != t.JSON_RIGHT_BRACKET:
        parsed_json, tokens = parse(tokens)
        array.append(parsed_json)
        if tokens[0] == t.JSON_COMMA:
            tokens = tokens[1:]
        else:
            raise lex.ParseException("Expected comma between objects in array")

    if tokens:
        return array, tokens[1:]
    else:
        raise lex.ParseException("Array has no closing bracket")


def parse_object(tokens):
    obj = {}
    index = 0
    while index < len(tokens) and tokens[index] != lex.JSON_RIGHT_BRACE:
        key = tokens[index]  # TODO: string validation and index validation
        assert key.startswith(t.JSON_QUOTE) and key.endswith(t.JSON_QUOTE)
        assert tokens[index + 1] == t.JSON_COLON
        value, index = parse(tokens[index + 2 :])
        obj[key] = value
    return obj
