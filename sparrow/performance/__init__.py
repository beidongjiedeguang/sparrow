import time
from ..string.color_string import rgb_string, color_const

__all__ = ['MeasureTime']


class MeasureTime:
    def __init__(self):
        self._cost_time = None
        self._start_time = None

    def start(self):
        self._start_time = time.time()

    def end(self):
        self._cost_time = time.time() - self._start_time

    def show_interval(self):
        self._cost_time = time.time() - self._start_time
        self._start_time = time.time()
        self._show_cost()
        return self.get_cost()

    def get_cost(self):
        return round(self._cost_time, 5)

    def _show_cost(self):
        cost_time = self.get_cost()
        rgb_cost_time = rgb_string(str(cost_time), color=color_const.GREEN)
        show_string = f"cost time: {rgb_cost_time}s"
        print(show_string)

