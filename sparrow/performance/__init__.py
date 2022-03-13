import time
from ..string.color_string import rgb_string, color_const

__all__ = ['TestTime']


class TestTime:
    def __init__(self):
        self._cost_time = None
        self._start_time = None

    def start(self):
        self._start_time = time.time()

    def end(self):
        self._cost_time = time.time() - self._start_time

    def show_interval(self):
        self._cost_time = time.time() - self._start_time
        self._show_cost()
        self._start_time = time.time()

    def _show_cost(self):
        cost_time = rgb_string(f"{self._cost_time:.3f}", color=color_const.GREEN)
        show_string = f"cost time: {cost_time}s"
        print(show_string)

