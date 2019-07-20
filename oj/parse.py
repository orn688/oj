from typing import Any, List, Tuple, Union

from oj.exceptions import InvalidJSON
from oj.tokens import Token, TokenType


class _BadToken(Exception):
    pass


def parse(tokens: List[Token]) -> List[Any]:
    index = 0
    if tokens[index].token_type == TokenType.OPEN_BRACKET:
        result, _ = parse_list(tokens, index)
        return result
    else:
        # TODO: JSON object parsing
        raise NotImplementedError()


def parse_list(tokens: List[Token], index: int) -> Tuple[List[Any], int]:
    """Parses a JSON list whose open bracket is at `index` in `tokens`."""
    assert tokens[index].token_type == TokenType.OPEN_BRACKET
    index += 1

    result_list: List[Any] = []
    expecting_value = True
    while index < len(tokens):
        token = tokens[index]
        if expecting_value:
            value, index = parse_value(tokens, index)
            result_list.append(value)
            # A comma or close bracket should come next, not another value.
            expecting_value = False
        else:
            index += 1
            if token.token_type == TokenType.COMMA:
                # Another value *must* come next. We can't have two commas in a row or
                # a comma immediately before a close bracket.
                expecting_value = True
            elif token.token_type == TokenType.CLOSE_BRACKET:
                # Found the end of the list.
                break
            else:
                raise InvalidJSON("expecting comma or close bracket")
    return result_list, index


def parse_value(
    tokens: List[Token], index: int
) -> Tuple[Any, int]:
    token = tokens[index]
    if token.token_type == TokenType.BOOLEAN:
        return parse_boolean(token), index + 1
    elif token.token_type == TokenType.NULL:
        return None, index + 1
    elif token.token_type == TokenType.OPEN_BRACKET:
        return parse_list(tokens, index)
    else:
        raise NotImplementedError(f"can't parse tokens of type {token.token_type.name}")


def parse_boolean(token: Token) -> bool:
    if token.lexeme == "true":
        return True
    elif token.lexeme == "false":
        return False
    else:
        raise _BadToken("invalid boolean lexeme")
