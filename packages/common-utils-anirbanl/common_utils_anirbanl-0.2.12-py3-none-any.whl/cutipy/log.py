import logging, sys, functools, os
import time
from cutipy.designpatterns import singleton

'''
Usage:
1. https://dev.to/aldo/implementing-logging-in-python-via-decorators-1gje
2. https://docs.python.org/3/howto/logging.html
'''


'''
Redirects stdout printing to python standard logging
From: https://wiki.python.org/moin/PythonDecoratorLibrary
'''
class LogPrinter:
    '''LogPrinter class which serves to emulates a file object and logs
       whatever it gets sent to a Logger object at the INFO level.'''
    def __init__(self, logger=None):
        '''Grabs the specific logger to use for logprinting.'''
        if logger is None:
            logger = logging.getLogger('logprinter')
            logging.basicConfig()
            logger.setLevel(logging.INFO)

        self.ilogger = logger


    def write(self, text):
        '''Logs written output to a specific logger'''
        if text.strip():
            self.ilogger.info(text)

def logprintinfo(func):
    '''Wraps a method so that any calls made to print get logged instead'''
    def pwrapper(*arg, **kwargs):
        stdobak = sys.stdout
        lpinstance = LogPrinter()
        sys.stdout = lpinstance
        try:
            return func(*arg, **kwargs)
        finally:
            sys.stdout = stdobak
    return pwrapper


'''
Logging decorator with specified logger (or default)
From: https://wiki.python.org/moin/PythonDecoratorLibrary

This decorator will log entry and exit points of your funtion using the specified logger or it defaults to your function's module name logger.

In the current form it uses the logging.INFO level, but it can easily customized to use what ever level. Same for the entry and exit messages.

Sample usage:

if __name__ == '__main__':
    logging.basicConfig()
    log = logging.getLogger('custom_log')
    log.setLevel(logging.DEBUG)
    log.info('ciao')

    @log_with(log)     # user specified logger
    def foo():
        print 'this is foo'
    foo()

    @log_with()        # using default logger
    def foo2():
        print 'this is foo2'
    foo2()
    
    
'''

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class log_with(object):
    '''Logging decorator that allows you to log with a
        specific logger.
    '''
    # Customize these messages
    ENTRY_MESSAGE = 'Entering {}'
    EXIT_MESSAGE = 'Exiting {}'

    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, func):
        '''Returns a wrapper that wraps func.
            The wrapper will log the entry and exit points of the function
            with logging.INFO level.
        '''
        # set logger if it was not set earlier
        if not self.logger:
            logging.basicConfig()
            self.logger = logging.getLogger(func.__module__)

        @functools.wraps(func)
        def wrapper(*args, **kwds):
            self.logger.info(self.ENTRY_MESSAGE.format(func.__name__))  # logging level .info(). Set to .debug() if you want to
            f_result = func(*args, **kwds)
            self.logger.info(self.EXIT_MESSAGE.format(func.__name__))   # logging level .info(). Set to .debug() if you want to
            return f_result
        return wrapper



'''
Custom logging decorator: Writing always to file 
Works by diverting output of print statement to log file created.

Inspired partly by: https://medium.com/swlh/add-log-decorators-to-your-python-project-84094f832181
and https://realpython.com/python-logging/

Usage below in logme decorator
'''
@singleton
class CustomLogger:
    def __init__(self, dir='.', filename=None, level=logging.DEBUG):
        if filename is None:
            filename = f"{__name__}-{time.time()}.log"
        if not os.path.exists(dir):
            os.makedirs(dir)

        self.logger = logging.getLogger(filename)
        file_handler = logging.FileHandler(os.path.join(dir, filename))
        file_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.setLevel(level)

    def __enter__(self):
        self.stdobak = sys.stdout
        lpinstance = LogPrinter(self.logger)
        sys.stdout = lpinstance
        return self

    def __exit__(self, *exc):
        sys.stdout = self.stdobak

'''
Usage: 

@logme
def myfunc(start=0, end=10, step=1):
    print(f"Starting with {start}")
    if start+step < end:
        myfunc(start+step, end, step)

'''
def logme(_func=None, *, logger=None):
    '''Wraps a method so that any calls made to print get logged instead'''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if logger is None:
                clog = CustomLogger()
            else:
                clog = logger
            with clog:
                value = func(*args, **kwargs)
            return value

        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)


