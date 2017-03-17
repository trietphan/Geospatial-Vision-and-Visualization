from itertools import (tee, islice, groupby)

def pairwise(iterable):
    '''s -> (s0,s1), (s1,s2), (s2, s3), ...
       from https://docs.python.org/3/library/itertools.html#itertools-recipes
    '''
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def in_chunks(iterable, size):
    '''s, 3 -> [s0,s1,s2], [s3,s4,s5], ...'''

    if '__len__' in dir(iterable):
        iterable = list(iterable)
        while iterable:
            chunk = iterable[:size]
            yield chunk
            iterable = iterable[size:]
        raise StopIteration
    else:
        while True:
            chunk = list(islice(iterable, size))
            if not chunk:
                raise StopIteration
            yield chunk

def add_items(dictionary, items):
    result = dictionary.copy()
    result.update(items)
    return result

def first(lst):
    return lst[0]

def last(lst):
    return lst[-1]

def group_by(key, lst):
    sorted_lst = sorted(lst, key=lambda e: getattr(e, key))
    return groupby(sorted_lst, key=lambda e: getattr(e, key))

def flatten(lst):
    return [item for sublst in lst for item in sublst]
