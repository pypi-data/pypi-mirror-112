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