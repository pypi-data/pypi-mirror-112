import functools
import time
import signal

def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")           # 4
        return value
    return wrapper_debug

def slow_down(_func=None, *, sleeptime=1):
    def decorator(func):
        """Sleep sleeptime seconds before calling the function"""
        @functools.wraps(func)
        def wrapper_slow_down(*args, **kwargs):
            print(f"Sleeping for {sleeptime} seconds.....")
            time.sleep(sleeptime)
            return func(*args, **kwargs)
        return wrapper_slow_down

    if _func is None:
        return decorator
    else:
        return decorator(_func)

def count_calls(func):
    @functools.wraps(func)
    def wrapper_count_calls(*args, **kwargs):
        wrapper_count_calls.num_calls += 1
        print(f"Call {wrapper_count_calls.num_calls} of {func.__name__!r}")
        return func(*args, **kwargs)
    wrapper_count_calls.num_calls = 0
    return wrapper_count_calls

def repeat(_func=None, *, num_times=2):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat

    if _func is None:
        return decorator_repeat
    else:
        return decorator_repeat(_func)


'''
Function Timeout
From: https://wiki.python.org/moin/PythonDecoratorLibrary

Sample Usage:

import time

@timeout(1, 'Function slow; aborted')
def slow_function():
    time.sleep(5)

'''

class TimeoutError(Exception): pass

def timeout(seconds, error_message = 'Function call timed out'):
    def decorated(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return functools.wraps(func)(wrapper)

    return decorated


'''
Use profiling/coverage using the decorators in https://github.com/mgedmin/profilehooks

@profile(immediate=True)
def add(number):
    import time
    time.sleep(2)
    if number > 1:
        print(f"Hello {number}")
    return number + 1
    
@timecall       # or @timecall(immediate=True)
def my_function(args, etc):
    pass
    
@coverage
def my_function(args, etc):
    pass
'''