import time
from ..string.color_string import rgb_string, color_const

__all__ = ['MeasureTime']


class MeasureTime:
    def __init__(self, prec=2, logger=None):
        self._cost_time = 0.
        self._start_time = time.time()
        self._logger = logger
        self._msg = None
        self._prec: int = prec

    def start(self):
        self._start_time = time.time()
        return self

    def end(self):
        self._cost_time = time.time() - self._start_time
        return self

    def show_interval(self, msg=None):
        self._msg = msg
        self._cost_time = time.time() - self._start_time
        self._start_time = time.time()
        self._show_cost()
        return self.get_cost()

    def get_cost(self):
        return f"{self._cost_time:.{int(self._prec)}E}"

    def _show_cost(self):
        cost_time = self.get_cost()
        msg = f"{self._msg}\t" if self._msg else ''
        if self._logger:
            show_string = f"{msg}cost time: {cost_time}s"
            self._logger.debug(show_string)
        else:
            rgb_cost_time = rgb_string(cost_time, color=color_const.GREEN)
            rgb_msg = rgb_string(f"{msg}", color=color_const.cyan)
            show_string = f"{rgb_msg}cost time: {rgb_cost_time}s"
            print(show_string)
