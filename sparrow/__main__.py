import fire
from sparrow.widgets import timer
from sparrow.multiprocess import start_server

func_list = [
    timer,
    start_server,
]
func_dict = {}
for func in func_list:
    func_dict[func.__name__] = func


def main():
    fire.Fire(func_dict)
