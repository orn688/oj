import oj


def test_loads_list():
    assert oj.loads("[true, false, true]") == [True, False, True]


def test_loads_nested_list():
    assert oj.loads("[true, [false, true]]") == [True, [False, True]]
    assert oj.loads("[true, [false, [true, false]]]") == [True, [False, [True, False]]]
