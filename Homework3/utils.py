from itertools import islice

def chunks(iterable, size):
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
