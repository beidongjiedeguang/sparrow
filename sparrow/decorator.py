from .color_str import rgb_string, GREEN, RED, BLUE
from functools import wraps, partial, update_wrapper
import logging
import inspect
import time


def test_time(times=10):
    # if func is None:
    #     return partial(time_it, times=times)
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            for i in range(times):
                func(*args, **kwargs)
            end = time.time()
            average_cost_time = (end-start)/times
            time_str = f"{average_cost_time:.3f}"

            print(f"Run {rgb_string(str(times), GREEN)} times, "
                  f"the average time is {rgb_string(time_str, GREEN)} seconds.")
            return func(*args, **kwargs)
        return wrapper
    return decorate


def runtime(func):
    """Log the runtime of the decorated function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        cost_time = end-start
        time_str = f"{cost_time:.3f}"
        print(f"Finished {rgb_string(func.__name__, RED)} in {rgb_string(time_str, GREEN)} secs.")
        return value
    return wrapper


def repeat(n=2):
    """repeat decorated function `n` times."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for i in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


def optional_debug(func):
    if 'debug' in inspect.signature(func).parameters:
        raise TypeError('debug argument already defined')

    debug_default = True

    @wraps(func)
    def wrapper(*args, debug=debug_default, **kwargs):
        if debug:
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            print(f"Calling '{func.__name__}({signature})'")
        value = func(*args, **kwargs)
        if debug:
            print(f"{func.__name__!r} returned {value!r}")
        return value
    sig = inspect.signature(func)
    parms = list(sig.parameters.values())
    parms.append(inspect.Parameter('debug',
                inspect.Parameter.KEYWORD_ONLY,
                default=debug_default))
    wrapper.__signature__ = sig.replace(parameters=parms)
    return wrapper


def count_calls(func):
    """Count the number of calls made to the decorated function. """
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.num_calls += 1
        print(f"Call {wrapper.num_calls} of {func.__name__!r}")
        return func(*args, **kwargs)
    wrapper.num_calls = 0
    return wrapper


class CountCalls:
    """Count the number of calls made to the decorated function."""

    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"Call {self.num_calls} of {self.func.__name__!r}")
        return self.func(*args, **kwargs)


class CallReminder:
    def __init__(self, func):
        self._func = func
        self._num_calls = 0
        
    def __call__(self, *args, **kwargs):
        self._num_calls += 1
        return self._func(*args, **kwargs)

    @property
    def count_calls(self):
        return self._num_calls


def logged(level, name=None, message=None):
    """
    Add logging to a function. level is the logging
    level, name is the logger name, and message is the
    log message. If name and message aren't specified,
    they default to the function's module and name.
    """
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)
        return wrapper
    return decorate
