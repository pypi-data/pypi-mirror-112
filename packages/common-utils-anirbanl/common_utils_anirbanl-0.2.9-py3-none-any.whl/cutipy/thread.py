from threading import Lock
from Queue import Queue

'''
Synchronized block execution
From: https://wiki.python.org/moin/PythonDecoratorLibrary

Sample Usage:

from threading import Lock
my_lock = Lock()

@synchronized(my_lock)
def critical1(*args):
    # Interesting stuff goes here.
    pass
    
'''

def synchronized(lock):
    '''Synchronization decorator.'''

    def wrap(f):
        def new_function(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return new_function
    return wrap

'''
Asynchronous Call
From: https://wiki.python.org/moin/PythonDecoratorLibrary

Sample Usage:

if __name__ == '__main__':
    # sample usage
    import time

    @asynchronous
    def long_process(num):
        time.sleep(10)
        return num * num

    result = long_process.start(12)

    for i in range(20):
        print i
        time.sleep(1)

        if result.is_done():
            print "result {0}".format(result.get_result())


    result2 = long_process.start(13)

    try:
        print "result2 {0}".format(result2.get_result())

    except asynchronous.NotYetDoneException as ex:
        print ex.message
'''

class asynchronous(object):
    def __init__(self, func):
        self.func = func

        def threaded(*args, **kwargs):
            self.queue.put(self.func(*args, **kwargs))

        self.threaded = threaded

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def start(self, *args, **kwargs):
        self.queue = Queue()
        thread = Thread(target=self.threaded, args=args, kwargs=kwargs);
        thread.start();
        return asynchronous.Result(self.queue, thread)

    class NotYetDoneException(Exception):
        def __init__(self, message):
            self.message = message

    class Result(object):
        def __init__(self, queue, thread):
            self.queue = queue
            self.thread = thread

        def is_done(self):
            return not self.thread.is_alive()

        def get_result(self):
            if not self.is_done():
                raise asynchronous.NotYetDoneException('the call has not yet completed its task')

            if not hasattr(self, 'result'):
                self.result = self.queue.get()

            return self.result

