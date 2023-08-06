def logic_or(p1, p2):
    assert(p1 >= 0 and p2 >= 0 and p1 < 2 and p2 < 2 and type(p1) is int and type(p2) is int)
    return p1+p2 != 0
    
def logic_and(p1, p2):
    assert(p1 >= 0 and p2 >= 0 and p1 < 2 and p2 < 2 and type(p1) is int and type(p2) is int)
    return p1*p2 == 1

def logic_xor(p1, p2):
    assert(p1 >= 0 and p2 >= 0 and p1 < 2 and p2 < 2 and type(p1) is int and type(p2) is int)
    return p1+p2 % 2 == 1


    