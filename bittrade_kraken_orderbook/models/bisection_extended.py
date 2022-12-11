# Adapted from https://docs.python.org/3/library/bisect.html
from bisect import bisect_left
def index(a, x, key=None):
    if not key:
        key = lambda w: w
    """Locate the leftmost value exactly equal to x"""
    i = bisect_left(a, x, key=key)
    if i != len(a) and key(a[i]) == x:
        return i
    raise ValueError