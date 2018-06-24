import math

from hypothesis import given, strategies as st

import oj


class TestLexNumber:
    # TODO: test arbitrary +/-

    @given(st.integers())
    def test_lex_int(self, x):
        assert oj.lex_number(str(x)) == (x, "")

    @given(st.floats(allow_infinity=False, allow_nan=False))
    def test_lex_float(self, x):
        assert oj.lex_number(str(x)) == (x, "")

    @given(
        st.floats(min_value=-1e15, max_value=1e15),
        st.integers(min_value=-10, max_value=10),
    )
    def test_lex_scientific_notation(self, base, exponent):
        json_input = f"{base}e{exponent}"
        num, left = oj.lex_number(json_input)
        print(json_input)
        assert math.isclose(num, base * 10 ** exponent)
        assert left == ""

    def test_lex_nan(self):
        num, rest = oj.lex_number("NaN")
        assert math.isnan(num)
        assert rest == ""

    def test_lex_infinity(self):
        assert oj.lex_number("Infinity") == (float("inf"), "")
        assert oj.lex_number("+Infinity") == (float("inf"), "")
        assert oj.lex_number("-Infinity") == (-float("inf"), "")

    def test_lex_number_no_number_before_decimal(self):
        assert oj.lex_number(".0") == (0.0, "")
