from . import lexer


def parse(tokens):
    if tokens[0] == lexer.JSON_LEFT_BRACKET:
        return parse_array(tokens[1:])
    elif tokens[0] == lexer.JSON_LEFT_BRACE:
        return parse_object(tokens[1:])
    else:
        return tokens[0], tokens[1:]


def parse_array(tokens):
    array = []

    while True:
        if tokens[0] == lexer.JSON_RIGHT_BRACKET:
            return array, tokens[1:]

        parsed_json, tokens = parse(tokens)
        array.append(parsed_json)
        if tokens[0] == lexer.JSON_COMMA:
            tokens = tokens[1:]
        else:
            raise lexer.ParseException("Expected comma between objects in array")

    raise lexer.ParseException("Array has no closing bracket")


def parse_object(tokens):
    return {}, tokens
