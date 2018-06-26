import math

from hypothesis import given, strategies as st

from oj import lexer


class TestLexNumber:
    # TODO: test arbitrary +/-

    @given(st.integers())
    def test_lex_int(self, x):
        assert lexer.lex_number(str(x)) == (x, "")

    @given(st.floats(allow_infinity=False, allow_nan=False))
    def test_lex_float(self, x):
        assert lexer.lex_number(str(x)) == (x, "")

    @given(
        st.floats(min_value=-1e15, max_value=1e15),
        st.integers(min_value=-10, max_value=10),
    )
    def test_lex_scientific_notation(self, base, exponent):
        json_input = f"{base}e{exponent}"
        num, left = lexer.lex_number(json_input)
        print(json_input)
        assert math.isclose(num, base * 10 ** exponent)
        assert left == ""

    def test_lex_nan(self):
        num, rest = lexer.lex_number("NaN")
        assert math.isnan(num)
        assert rest == ""

    def test_lex_infinity(self):
        assert lexer.lex_number("Infinity") == (float("inf"), "")
        assert lexer.lex_number("+Infinity") == (float("inf"), "")
        assert lexer.lex_number("-Infinity") == (-float("inf"), "")

    def test_lex_float_no_digits_before_decimal(self):
        assert lexer.lex_number(".0") == (0.0, "")

    def test_lex_int_no_digits_after_decimal(self):
        assert lexer.lex_number("1.") == (1, "")


class TestLexString:
    @given(st.from_regex(r'^[^"]*$'))
    def test_lex_string(self, string):
        assert lexer.lex_string(f'"{string}"') == (lexer.JSONString(string), "")


class TestLexBool:
    def test_lex_true(self):
        assert lexer.lex_bool("true") == (True, "")

    def test_lex_false(self):
        assert lexer.lex_bool("false") == (False, "")
