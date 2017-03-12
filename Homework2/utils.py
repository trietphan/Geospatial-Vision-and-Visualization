from itertools import tee

def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ...
       from https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
