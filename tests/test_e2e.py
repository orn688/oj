import oj


def test_loads_list():
    assert oj.loads("[true, false, null]") == [True, False, None]


def test_loads_nested_list():
    assert oj.loads("[true, [false, true]]") == [True, [False, True]]
    assert oj.loads("[true, [false, [true, null]]]") == [True, [False, [True, None]]]
