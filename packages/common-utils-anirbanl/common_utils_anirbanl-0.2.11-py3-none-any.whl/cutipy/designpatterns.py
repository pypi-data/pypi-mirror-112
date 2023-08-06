import functools

'''
Usage from: https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python

#Python3
class MyClass(BaseClass, metaclass=Singleton):
    pass
'''
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

'''
Usage from https://realpython.com/primer-on-python-decorators/
'''
def singleton(cls):
    """Make a class a Singleton class (only one instance)"""
    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance
    wrapper_singleton.instance = None
    return wrapper_singleton


'''
Decorator Factory: https://www.bbayles.com/index/decorator_factory

Returns decorator functions (capable of taking decorator-specific arguments to produce decorator) around generator functions/iterables
Allows chaining of such returned decorators


Usage 1:
enumerator = decorator_factory(enumerate)
accumulator = decorator_factory(itertools.accumulate)

enumerator_1 = enumerator(start=1)
accumulator_add = accumulator()
@enumerator_1
@accumulator_add
def collatz(x):
    # ...

Usage 2:
accumulator = decorator_factory(itertools.accumulate)
dropper = decorator_factory(itertools.dropwhile, 1)

@dropper(lambda x: x < 50)
@accumulator()
def collatz(x):
    # ...


Usage 3:
taker = decorator_factory(itertools.takewhile, 1)

@taker(lambda x : x > 150)
def mygen(num=100):
    x = num
    while True:
        x += 1
        yield x-1
'''
def decorator_factory(wrapping_func, result_index=0):
    def decorator(*wrapping_args, **wrapping_kwargs):
        def outer_wrapper(f):
            @functools.wraps(f)
            def inner_wrapper(*args, **kwargs):
                result = f(*args, **kwargs)
                wrapping_args_ = list(wrapping_args)
                wrapping_args_.insert(result_index, result)
                return wrapping_func(*wrapping_args_, **wrapping_kwargs)

            return inner_wrapper

        return outer_wrapper

    return decorator