import json
from string import printable

import pytest
from hypothesis import given
from hypothesis import strategies as st

import oj


@st.composite
def raw_json(draw):
    strategy = st.recursive(
        st.none() | st.booleans() | st.floats(allow_nan=True, allow_infinity=True)
        # JSON doesn't technically have integers, but all Python floats have decimal
        # places when passed through json.dumps() and we want to test parsing of JSON
        # numbers without decimal places too.
        | st.integers() | st.text(printable),
        lambda children: (
            st.lists(children) | st.dictionaries(st.text(printable), children)
        ),
    )
    python_object = draw(strategy)
    return json.dumps(python_object, indent=2)


def assert_json_equal(object1, object2):
    """Assert that two parsed JSON entities are equal.

    Takes into account several issues that prevent us from simply using
    `object1 == object2` all the time:
    - Floating point error
    - NaN != NaN

    pytest.approx() handles both of these when based an `abs` argument and with
    `nan_ok` set.
    """
    assert type(object1) == type(object2)
    if isinstance(object1, float):
        assert pytest.approx(object1, object2, abs=1e-20, nan_ok=True)
    elif isinstance(object1, list):
        assert len(object1) == len(object2)
        for item1, item2 in zip(object1, object2):
            assert_json_equal(item1, item2)
    elif isinstance(object1, dict):
        assert len(object1) == len(object2)
        for key in object1:
            assert key in object2
            assert_json_equal(object1[key], object2[key])
    else:
        # This is a simple object (e.g. string or bool), so fall back to a regular
        # equality check.
        assert object1 == object2


@given(raw_json())
def test_compared_to_stdlib(input_json):
    assert_json_equal(oj.loads(input_json), json.loads(input_json))
