from sparrow.performance import MeasureTime
import time


def test_show_time():
    tt = MeasureTime()
    tt.start()
    time.sleep(0.1)
    tt.show_interval()
    time.sleep(0.12)
    tt.show_interval()
