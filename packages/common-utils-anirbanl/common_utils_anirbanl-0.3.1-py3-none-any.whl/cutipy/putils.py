import attr
import functools, operator
from pathlib import Path
from cutipy.deepdict import *
from collections import abc

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

def deserialize_hp(s, separator=None):
    spliterator = [] if separator is None else [separator]
    hp = deepdict()
    for kv in s.strip().split(*spliterator):
        k, v = kv.strip().split("=")
        v = parse_value(v)
        hp[k] = v
    return hp

def serialize_hp(hp, separator=" "):
    return separator.join(f"{path}={value}" for path, value in sorted(hp.Leaves(), key=lambda kv: kv[0]))

def dump_hp(path, hp):
    s = serialize_hp(hp, separator="\n")
    Path(path).write_text(s)

def load_hp(path):
    return deserialize_hp(Path(path).read_text())

def deepitems(dikt, _path=()):
    if isinstance(dikt, abc.Mapping):
        for key, value in dikt.items():
            yield from deepitems(value, _path + (key,))
    else:
        yield _path, dikt

def deepsetitem(dikt, path, value):
    while True:
        key, *path = path
        if not path:
            dikt[key] = value
            break
        dikt = dikt.setdefault(key, dict())

