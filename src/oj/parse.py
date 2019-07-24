from typing import Any, List, Optional, Tuple, Union

from oj.exceptions import InvalidJSON
from oj.tokens import Token, TokenType


class _BadToken(AssertionError):
    pass


def parse(tokens: List[Token]) -> Union[None, bool, float, str, list, dict]:
    value, next_index = parse_value(tokens, 0)
    if next_index != len(tokens):
        raise InvalidJSON("more than one value at top level of json")
    return value


def parse_value(tokens: List[Token], index: int) -> Tuple[Any, int]:
    token = tokens[index]
    if token.token_type == TokenType.NULL:
        assert token.lexeme == "null", "null token lexeme must be 'null'"
        return None, index + 1
    elif token.token_type == TokenType.BOOLEAN:
        return parse_boolean(token), index + 1
    elif token.token_type == TokenType.STRING:
        return parse_string(token), index + 1
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
                raise InvalidJSON("expecting comma or close bracket in list")
    return result_list, index
