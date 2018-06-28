import math

from hypothesis import given, strategies as st

from oj import lexer

any_sign = st.from_regex(r"^[+-]?$")


@given(st.integers())
def test_lex_int(x):
    assert lexer.lex_number(str(x)) == (x, "")


@given(st.floats(allow_infinity=False, allow_nan=False))
def test_lex_float(x):
    assert lexer.lex_number(str(x)) == (x, "")


@given(
    st.floats(min_value=-1e15, max_value=1e15), st.integers(min_value=-10, max_value=10)
)
def test_lex_scientific_notation(base, exponent):
    num, left = lexer.lex_number(f"{base}e{exponent}")
    assert math.isclose(num, base * 10 ** exponent)
    assert left == ""


def test_lex_nan():
    num, rest = lexer.lex_number("NaN")
    assert math.isnan(num)
    assert rest == ""


def test_lex_infinity():
    assert lexer.lex_number("Infinity") == (float("inf"), "")
    assert lexer.lex_number("+Infinity") == (float("inf"), "")
    assert lexer.lex_number("-Infinity") == (-float("inf"), "")


def test_lex_float_no_digits_before_decimal():
    assert lexer.lex_number(".0") == (0.0, "")


def test_lex_int_no_digits_after_decimal():
    assert lexer.lex_number("1.") == (1, "")


def test_lex_plus_sign():
    assert lexer.lex_number("+1") == (1, "")


@given(st.from_regex(r'^[^"]*$'))  # Just avoid double quotes
def test_lex_string(string):
    assert lexer.lex_string(f'"{string}"') == (lexer.JSONString(string), "")


def test_lex_true():
    assert lexer.lex_bool("true") == (True, "")


def test_lex_false():
    assert lexer.lex_bool("false") == (False, "")


def test_lex_null():
    assert lexer.lex_null("null") == (lexer.JSONNull(), "")
