import json
from string import printable

from hypothesis import given
from hypothesis import strategies as st

import oj


@st.composite
def raw_json(draw):
    strategy = st.recursive(
        st.none() | st.booleans() | st.text(printable),  # st.floats() |
        lambda children: (
            st.lists(children, 1)
            | st.dictionaries(st.text(printable), children, min_size=1)
        ),
    )
    python_object = draw(strategy)
    return json.dumps(python_object, indent=2)


@given(raw_json())
def test_compared_to_stdlib(input_json):
    assert oj.loads(input_json) == json.loads(input_json)
