import logging, sys, functools

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
    def __init__(self):
        '''Grabs the specific logger to use for logprinting.'''
        self.ilogger = logging.getLogger('logprinter')
        il = self.ilogger
        logging.basicConfig()
        il.setLevel(logging.INFO)

    def write(self, text):
        '''Logs written output to a specific logger'''
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