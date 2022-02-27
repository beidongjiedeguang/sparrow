import keyboard
import time
from collections import deque
from sparrow.string.color_string import rgb_string
from sparrow.color.constant import TEAL, GREEN


def timer(dt=0.01):
    """A simple timer.
    Press `space` to start and suspend.
    press `q` to quit.
    """
    print(
        rgb_string("Press `space` to start and suspend.", color=TEAL),
    )
    q = deque(maxlen=1)
    q.append(True)
    keyboard.wait("space")
    keyboard.add_hotkey("space", lambda: q.append(not q[0]))
    t0 = time.time()
    current_time = 0
    while True:
        time.sleep(dt)
        ct = time.time()
        if q[0]:
            t0 = ct
        else:
            current_time += ct - t0
            print(rgb_string(f"\r{current_time:.3f} secs", color=GREEN), end="")
            t0 = ct
        if keyboard.is_pressed("q"):
            break
