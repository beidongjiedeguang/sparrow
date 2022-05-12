from ..string.color_string import rgb_string, color_const
from ..log.core import BaseLogger, SimpleLogger
from functools import wraps, update_wrapper
import logging
import inspect
import time
import types
from typing import Union


class TryDecorator:
    def __init__(self, error_return=None, logger: Union[SimpleLogger, None] = None):
        self.error_return = error_return
        self.logger = logger

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"{func.__name__} raised an exception: {e}")
                else:
                    print(f"{func.__name__} raised an exception: {e}")
                result = self.error_return
            return result

        return wrapper

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


def try_decorator(error_return=None, logger: Union[SimpleLogger, None] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                value = func(*args, **kwargs)
            except Exception as e:
                if logger:
                    logger.warning(f"{func.__name__} error: {e}")
                else:
                    print(f"{func.__name__} error: {e}")
                return error_return
            return value

        return wrapper

    return decorator


def benchmark(times=10, logger: Union[SimpleLogger, None] = None, level=logging.INFO, ):
    # if func is None:
    #     return partial(time_it, times=times)
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            value = None
            for i in range(times):
                value = func(*args, **kwargs)
            end = time.time()
            average_cost_time = (end - start) / times
            time_str = f"{average_cost_time:.3f}"

            if logger:
                logger.log(
                    level,
                    f"Run {rgb_string(str(times), color_const.GREEN)} times, "
                    f"the average time is {rgb_string(time_str, color_const.GREEN)} seconds."
                )
            else:
                print(
                    f"Run {rgb_string(str(times), color_const.GREEN)} times, "
                    f"the average time is {rgb_string(time_str, color_const.GREEN)} seconds."
                )
            return value

        return wrapper

    return decorate


def measure_time(logger: Union[SimpleLogger, None] = None, level=logging.INFO):
    def decorate(func):
        """Log the runtime of the decorated function."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            value = func(*args, **kwargs)
            end = time.time()
            cost_time = end - start
            time_str = f"{cost_time:.3f}"
            if logger:
                logger.log(level,
                           f"Finished {rgb_string(func.__name__, color_const.RED)} in {rgb_string(time_str, color_const.GREEN)} secs."
                           )
            else:
                print(f"Finished {rgb_string(func.__name__, color_const.RED)} in {rgb_string(time_str, color_const.GREEN)} secs.")
            return value

        return wrapper

    return decorate


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
    if "debug" in inspect.signature(func).parameters:
        raise TypeError("debug argument already defined")

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
    parms.append(
        inspect.Parameter(
            "debug", inspect.Parameter.KEYWORD_ONLY, default=debug_default
        )
    )
    wrapper.__signature__ = sig.replace(parameters=parms)
    return wrapper


def count_calls(func):
    """Count the number of calls made to the decorated function."""

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


def singleton(cls):
    """
    Usage
    -----
        @singleton
        class Cls:
            pass
    """
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


class Singleton:
    """
    Usage
    -----
        @Singleton
        class Cls:
            pass
    """

    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]


class MetaSingleton(type):
    """
    Usage
    -----
        class Cls(metaclass=MetaSingleton):
            pass
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
