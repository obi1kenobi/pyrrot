from itertools import repeat

def constant_factory(value):
    return repeat(value).next
