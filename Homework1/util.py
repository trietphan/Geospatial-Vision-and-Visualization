def pipe_through(*fns):
    def result_fn(datum):
        acc = datum
        for fn in list(fns):
            acc = fn(acc)
        return acc

    return result_fn

def last(lst):
    return lst[-1]
