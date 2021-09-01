from get_row_api import func1, cnt_letters, fact


def test_func1():
    assert func1(3,3) == 9

def test_cnt_letters():
    assert cnt_letters("test") == 4

def test_fact():
    assert fact(12) == 479001600