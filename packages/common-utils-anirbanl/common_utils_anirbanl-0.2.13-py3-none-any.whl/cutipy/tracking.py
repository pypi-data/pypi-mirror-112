import time, functools
from collections import OrderedDict, deque
from cutipy.designpatterns import singleton

@singleton
class Timer:
    def __init__(self):
        self.dts = OrderedDict()
        self.starts = OrderedDict()
        self.names = deque()

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *exc):
        end_time = time.time()
        name_popped = self.names.pop()
        self.dts[name_popped] = end_time - self.starts[name_popped]

    def register(self, name):
        self.names.append(name)
        self.starts[name] = self.start_time

    def __repr__(self):
        s = ''
        for k,v in self.dts.items():
            s = s + f"{k} : {v} secs\n"
        return s

    def purge(self):
        self.dts = OrderedDict()

def timeme(_func=None, *, timer=Timer()):
    def decorator(func):
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            with timer:
                timer.register(f"Function {func.__name__!r} Call at {time.time()}")
                value = func(*args, **kwargs)
            return value

        return wrapper_timer

    if _func is None:
        return decorator
    else:
        return decorator(_func)
