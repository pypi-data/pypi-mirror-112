import attr
import functools, operator

# decorator with *args, **kwargs appended
def decorator(decorator):
    def decorator_factory(*args, **kwargs):
        def decorated(function):
            return decorator(function, *args, **kwargs)
        return decorated
    return decorator_factory

# decorator to immediately call the decorated object
def call(*args, **kwargs):
    def decorator(decoratee):
        return decoratee(*args, **kwargs)
    return decorator

def functiontable(cls):
    return FunctionTable(vars(cls))

@attr.s
class FunctionTable:
    dikt = attr.ib(factory=dict)
    def __getitem__(self, key):
        return self.dikt[key]
    __getattr__ = __getitem__

def all_equal(xs):
    xs = list(xs)
    return all(x == xs[0] for x in xs)

def the_unique(xs):
    xs = list(xs)
    assert xs
    assert all_equal(xs)
    return xs[0]

def eqzip(*xs):
    xs = tuple(map(list, xs))
    assert all_equal(map(len, xs))
    return zip(*xs)

def zipitems(*dikts):
    dikts = list(dikts)
    assert all_equal(map(set, dikts))
    for key in dikts[0]:
        yield key, tuple(dikt[key] for dikt in dikts)

def zipdict(*dikts):
    return dict(zipitems(*dikts))

def unzip(tuples, rank=None):
    if not tuples:
        # if there are zero tuples, then for consistency we should return
        # an empty sequence for each element the tuples otherwise would have.
        # we don't know how many, so unless the caller explicitly tells us,
        # we can't support this case.
        if rank is None:
            raise ValueError("cannot unzip empty iterable without knowing rank of tuples")
        return tuple([] for _ in range(rank))
    return tuple(map(list, eqzip(*tuples)))

def mean(xs, default_zero=True):
    xs = list(xs)
    if default_zero and not xs: return 0
    return sum(xs) / len(xs)

def prod(xs):
    return functools.reduce(operator.mul, xs, 1)

def parse_value(s):
    s = s.strip()
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s

