from oj import lex, parse


def loads(string):
    tokens, _ = lex.lex(string)
    # TODO: assert no remainder
    return parse(tokens)
