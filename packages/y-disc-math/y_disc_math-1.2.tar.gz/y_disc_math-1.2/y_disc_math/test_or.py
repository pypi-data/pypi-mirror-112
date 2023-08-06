from .first_order_logic import logic_or

def test_0_0():
    p1 = 0
    p2 = 0
    assert(logic_or(p1, p2) == 0)

def test_0_1():
    p1 = 0
    p2 = 1
    assert(logic_or(p1, p2) == 1)

def test_1_0():
    p1 = 1
    p2 = 0
    assert(logic_or(p1, p2) == 1)

def test_1_1():
    p1 = 1
    p2 = 1
    assert(logic_or(p1, p2) == 1)
