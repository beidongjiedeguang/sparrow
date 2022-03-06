from functools import wraps
import inspect
import os

__all__ = ["get_func_param_dict"]


def get_func_param_dict():
    frame = inspect.currentframe().f_back
    args, varargs, keywords, loc = inspect.getargvalues(frame)
    target_dict = {}
    for key in args:
        target_dict[key] = loc[key]
    return target_dict


# Useless
def findcaller(func):
    @wraps(func)
    def wrapper(*args):
        currentframe = inspect.currentframe()
        f = currentframe.f_back
        file_name = os.path.basename(f.f_code.co_filename)
        func_name = f.f_code.co_name
        line_num = f.f_lineno

        args = list(args)
        args.append(f"{os.path.basename(file_name)}.{func_name}.{line_num}")
        func(*args)

    return wrapper
