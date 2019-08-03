import json
from string import printable

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

import oj
from oj.exceptions import JSONDecodeError


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


@st.composite
def corrupted_json(draw):
    """Generates raw JSON strings with one character removed.

    The intention is to generate inputs that are likely to trigger corner cases and
    find bugs in the parsing of malformed inputs.
    """
    original = draw(raw_json())
    # original should never be empty (the shortest it can be is a single digit) so it's
    # safe to remove a random character.
    index_to_remove = draw(st.integers(0, len(original)))
    return original[: index_to_remove - 1] + original[index_to_remove:]


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
@pytest.mark.fuzz
def test_compared_to_stdlib_success(input_json):
    assert_json_equal(oj.loads(input_json), json.loads(input_json))


@given(corrupted_json())
@settings(max_examples=200)
@pytest.mark.fuzz
def test_compared_to_stdlib_corrupted_json(input_json):
    # Randomly removing a character isn't guaranteed to make the input invalid (e.g.,
    # if we happen to remove a character from the middle of a string), so it's possible
    # that parsing the input shouldn't raise an exception. Therefore, we only care that
    # oj.loads(x) raises an exception iff json.loads(x) raises an exception for all
    # strings x.
    try:
        json.loads(input_json)
    except json.JSONDecodeError:
        stdlib_raises = True
    else:
        stdlib_raises = False

    try:
        oj_result = oj.loads(input_json)
    except JSONDecodeError as exc:
        oj_raises = True
        oj_result = exc
    else:
        oj_raises = False

    assert stdlib_raises == oj_raises, oj_result


@given(st.text())
@settings(max_examples=2000)
@pytest.mark.fuzz
def test_compared_to_stdlib_random_text(input_text):
    try:
        json.loads(input_text)
    except json.JSONDecodeError:
        stdlib_raises = True
    else:
        stdlib_raises = False

    try:
        oj_result = oj.loads(input_text)
    except oj.JSONDecodeError as exc:
        oj_raises = True
        oj_result = exc
    else:
        oj_raises = False

    assert stdlib_raises == oj_raises, oj_result
