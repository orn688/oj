import math

from hypothesis import given, strategies as st

from oj import lex

any_sign = st.from_regex(r"^[+-]?$")


def json_characters():
    return st.text(alphabet=lex.JSON_SEPARATORS + lex.JSON_WHITESPACE)


@given(st.integers(), json_characters())
def test_lex_int(value, suffix):
    token, remainder = lex.lex_number(str(value) + suffix)
    assert token.value == value
    assert remainder == suffix


@given(st.floats(allow_infinity=False, allow_nan=False), json_characters())
def test_lex_float(value, suffix):
    token, remainder = lex.lex_number(str(value) + suffix)
    assert token.value == value
    assert remainder == suffix


@given(
    st.floats(min_value=-1e15, max_value=1e15),
    st.integers(min_value=-10, max_value=10),
    json_characters(),
)
def test_lex_scientific_notation(base, exponent, suffix):
    token, remainder = lex.lex_number(f"{base}e{exponent}" + suffix)
    assert math.isclose(token.value, base * 10 ** exponent)
    assert remainder == suffix


@given(json_characters())
def test_lex_nan(suffix):
    token, remainder = lex.lex_number("NaN" + suffix)
    assert math.isnan(token.value)
    assert remainder == suffix


@given(st.from_regex(r"\+?Infinity", fullmatch=True), json_characters())
def test_lex_positive_infinity(value, suffix):
    token, remainder = lex.lex_number(value + suffix)
    assert token.value == math.inf
    assert remainder == suffix


@given(json_characters())
def test_lex_negative_infinity(suffix):
    token, remainder = lex.lex_number("-Infinity" + suffix)
    assert token.value == -math.inf
    assert remainder == suffix


# TODO: rejection testing e.g., (".1" and "1.") are not valid JSON.


@given(st.integers(min_value=1), json_characters())
def test_lex_plus_sign(value, suffix):
    token, remainder = lex.lex_number(f"+{value}" + suffix)
    assert token.value == value
    assert remainder == suffix


@given(st.from_regex(r'^[^"]*$'), json_characters())
def test_lex_string(string, suffix):
    token, remainder = lex.lex_string(f'"{string}"' + suffix)
    assert token.value == string
    assert remainder == suffix


@given(json_characters())
def test_lex_true(suffix):
    token, remainder = lex.lex_bool("true" + suffix)
    assert token.value is True
    assert remainder == suffix


@given(json_characters())
def test_lex_false(suffix):
    token, remainder = lex.lex_bool("false" + suffix)
    assert token.value is False
    assert remainder == suffix


@given(json_characters())
def test_lex_null(suffix):
    token, remainder = lex.lex_null("null" + suffix)
    assert token.value is None
    assert remainder == suffix
