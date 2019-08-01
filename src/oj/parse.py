import math
from typing import Any, Dict, List, Optional, Tuple, Union

from oj.exceptions import InvalidJSON
from oj.tokens import Token, TokenType


def parse(tokens: List[Token]) -> Union[None, bool, float, str, list, dict]:
    value, next_index = parse_value(tokens, 0)
    if next_index != len(tokens):
        raise InvalidJSON("more than one value at top level of json")
    return value


def parse_value(tokens: List[Token], index: int) -> Tuple[Any, int]:
    if index >= len(tokens):
        raise InvalidJSON(f"expecting value at index {index}")
    token = tokens[index]
    if token.token_type == TokenType.NULL:
        assert token.lexeme == "null", "null token lexeme must be 'null'"
        return None, index + 1
    elif token.token_type == TokenType.BOOLEAN:
        return parse_boolean(token), index + 1
    elif token.token_type == TokenType.NUMBER:
        return parse_number(token), index + 1
    elif token.token_type == TokenType.INFINITY:
        if token.lexeme == "Infinity":
            return math.inf, index + 1
        elif token.lexeme == "-Infinity":
            return -math.inf, index + 1
        assert False, "invalid infinity lexeme"
    elif token.token_type == TokenType.NAN:
        assert token.lexeme == "NaN", "NaN token lexeme must be 'NaN'"
        return math.nan, index + 1
    elif token.token_type == TokenType.STRING:
        return parse_string(token), index + 1
    elif token.token_type == TokenType.OPEN_BRACKET:
        return parse_array(tokens, index)
    elif token.token_type == TokenType.OPEN_BRACE:
        return parse_object(tokens, index)
    else:
        raise InvalidJSON(f"expecting value at index {index}")


def parse_boolean(token: Token) -> bool:
    if token.lexeme == "true":
        return True
    elif token.lexeme == "false":
        return False
    else:
        assert False, "invalid boolean lexeme"


def parse_number(token: Token) -> Union[int, float]:
    number: Union[int, float]
    literal = token.lexeme
    number, index = _parse_integer(literal)

    if index < len(literal) and literal[index] == ".":
        number = float(number)
        index += 1
        decimal_places = 0
        while index < len(literal) and literal[index].isdigit():
            decimal_places += 1
            number += _parse_digit(literal[index]) / (10 ** decimal_places)
            index += 1
        if decimal_places == 0:
            raise InvalidJSON("no decimal places after period")

    if index < len(literal) and literal[index].lower() == "e":
        exponent, index = _parse_integer(
            literal, index + 1, allow_plus=True, allow_leading_zeros=True
        )
        number = float(number) * (10 ** exponent)

    if index < len(literal):
        raise InvalidJSON("unexpected characters after number")

    return number


def _parse_integer(
    literal: str,
    start_index: int = 0,
    allow_plus: bool = False,
    allow_leading_zeros: bool = False,
) -> Tuple[int, int]:
    if start_index >= len(literal):
        raise InvalidJSON("expected number")

    is_negative = literal[start_index] == "-"
    if literal[start_index] == "-" or (allow_plus and literal[start_index] == "+"):
        start_index += 1

    index = start_index
    integer = 0
    # We could just use the int(str) function, but that would be cheating.
    while index < len(literal) and literal[index].isdigit():
        integer *= 10
        integer += _parse_digit(literal[index])
        index += 1

    if index == start_index:
        raise InvalidJSON("expected number")

    if (
        not allow_leading_zeros
        and literal[start_index] == "0"
        and index - start_index > 1
    ):
        raise InvalidJSON("leading zeros in number")

    if is_negative:
        integer *= -1
    return integer, index


def _parse_digit(digit: str) -> int:
    # Again, int() is easy but cheating.
    return ord(digit) - ord("0")


def parse_string(token: Token) -> str:
    has_quotes = token.lexeme.startswith('"') and token.lexeme.endswith('"')
    assert has_quotes, "string lexeme not quoted"

    chars: List[str] = []
    escaped = False
    current_unicode_literal: Optional[List[str]] = None
    for i in range(1, len(token.lexeme) - 1):
        char = token.lexeme[i]
        if current_unicode_literal is not None:
            current_unicode_literal.append(char)
            if len(current_unicode_literal) == 4:
                try:
                    char_point = int("".join(current_unicode_literal), base=16)
                except ValueError:
                    raise InvalidJSON("invalid hex in unicode literal")
                chars.append(chr(char_point))
                current_unicode_literal = None
        elif not escaped and char == "\\":
            # Backlash; escape the next character.
            escaped = True
        elif escaped:
            # The previous character was a backslash.
            escaped = False
            if char == "u":
                current_unicode_literal = []
            else:
                try:
                    escape_char = {
                        "b": "\b",
                        "f": "\f",
                        "n": "\n",
                        "r": "\r",
                        "t": "\t",
                        '"': '"',
                        "/": "/",
                        "\\": "\\",
                    }[char]
                except KeyError:
                    raise InvalidJSON("invalid \\escape")
                chars.append(escape_char)
        else:
            # Regular old character.
            chars.append(char)

    if current_unicode_literal is not None:
        raise InvalidJSON("unterminated unicode literal")
    if escaped:
        raise InvalidJSON("unterminated escape sequence")

    return "".join(chars)


def parse_array(tokens: List[Token], index: int) -> Tuple[List[Any], int]:
    """Parses a JSON list whose open bracket is at `index` in `tokens`."""
    assert tokens[index].token_type == TokenType.OPEN_BRACKET
    index += 1
    if index >= len(tokens):
        raise InvalidJSON("unterminated array")

    result_list: List[Any] = []
    if tokens[index].token_type == TokenType.CLOSE_BRACKET:
        # Empty list.
        return result_list, index + 1

    expecting_value = True
    while index < len(tokens):
        token = tokens[index]
        # TODO: what if the list is empty?
        if expecting_value:
            value, index = parse_value(tokens, index)
            result_list.append(value)
            # A comma or close bracket should come next, not another value.
            expecting_value = False
        else:
            if token.token_type == TokenType.COMMA:
                # Another value *must* come next. We can't have two commas in a row or
                # a comma immediately before a close bracket.
                expecting_value = True
                index += 1
            elif token.token_type == TokenType.CLOSE_BRACKET:
                # Found the end of the list.
                break
            else:
                raise InvalidJSON("expecting comma or close bracket in list")
    return result_list, index + 1


def parse_object(tokens: List[Token], index: int) -> Tuple[Dict[str, Any], int]:
    assert tokens[index].token_type == TokenType.OPEN_BRACE
    index += 1
    if index >= len(tokens):
        raise InvalidJSON("unterminated object")

    result_dict: Dict[str, Any] = {}
    if tokens[index].token_type == TokenType.CLOSE_BRACE:
        # Empty dict.
        return result_dict, index + 1

    expecting_value = True
    expecting_colon = False
    current_key: Optional[str] = None
    while index < len(tokens):
        token = tokens[index]
        # TODO: what if the dict is empty?
        if expecting_value:
            if current_key is None:
                if token.token_type != TokenType.STRING:
                    raise InvalidJSON("object keys must be strings")
                current_key = parse_string(token)
                expecting_colon = True
                index += 1
            else:
                value, index = parse_value(tokens, index)
                result_dict[current_key] = value
                current_key = None
            expecting_value = False
        elif expecting_colon:
            if token.token_type != TokenType.COLON:
                raise InvalidJSON(f"expected colon at index {index}")
            expecting_colon = False
            expecting_value = True
            index += 1
        else:
            # We reached the end of a key/value pair, so we expect either a comma, or a
            # close brace to end the object.
            if token.token_type == TokenType.COMMA:
                expecting_value = True
                index += 1
            elif token.token_type == TokenType.CLOSE_BRACE:
                # Found the end of the object.
                break
            else:
                raise InvalidJSON(f"expected comma or close brace at index {index}")
    return result_dict, index + 1
