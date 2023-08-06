'''

Author: Zeng Siwei
Date: 2021-01-29 16:17:21
LastEditors: Zeng Siwei
LastEditTime: 2021-04-02 11:25:32
Description: 

'''
from contextlib import ContextDecorator
import time

class Timer(ContextDecorator):
    '''

    Functions: 
        start(idx): Start Timer
        stop(idx): Stop Timer
        get(idx, accum): Get (accumulating) runtime
        log(idx, accum): Output (accumulating) runtime
        delete(idx)
        clear
	
    Usage: 
        t = Timer()

        t.start("doxxx")
        # do something
        t.stop("doxxx")
    '''

    def __init__(self, cum = False):
        self.start_time = dict()
        self.end_time = dict()
        self.accum_time = dict()

    def start(self, idx = ""):
        self.start_time[idx] = time.time()

    def stop(self, idx = "", log = False):
        if self.start_time.get(idx, None) is None:
            raise ValueError(f"Timer is not running. Use .start() to start it")

        self.end_time[idx] = time.time()

        run_time = self.end_time[idx]-self.start_time[idx]
        self.accum_time[idx] = self.accum_time.get(idx, 0) + run_time
        
        if log:
            self.log(idx)
        return run_time

    def get(self, idx, accum = True):
        if accum:
            return self.accum_time[idx]
        else:
            run_time = self.end_time[idx]-self.start_time[idx]
            return run_time
        
    def log(self, idx, accum = True):
        str_out = "Code %s runs %s sec" % (idx, self.get(idx, accum))
        
        if accum:
            str_out += " in total"
        print(str_out)

    def delete(self, idx):
        self.start_time.pop(idx)
        self.end_time.pop(idx)
        self.accum_time.pop(idx)

    def clear(self):
        self.start_time.clear()
        self.end_time.clear()
        self.accum_time.clear()

    def __enter__(self, idx=""):
        self._context_idx = idx
        self.start(self._context_idx)
        return self

    def __exit__(self, *args):
        self.stop(self._context_idx, log=True)
        self.clear()


def test_context_manager(num):
    for i in range(num):
            y = i**2 + 5*(i**8) + i


@Timer()
def test_decorator(num):
    for i in range(num):
            y = i**2 + 5*(i**8) + i

if __name__ == "__main__":
    t = Timer()

    # test function
    accum = 0
    for i in range(1000):
        t.start("doxxx")
        y = i**2 + 5*(i**8) + i
        run = t.stop("doxxx", True)
        accum += run
    t.log("doxxx", accum=True)
    print(accum)

    # test context manager
    with Timer():
        test_context_manager(1000000)

    # test decorator
    test_decorator(1000000)