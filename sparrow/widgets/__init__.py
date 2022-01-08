import keyboard
import time
from collections import deque
from sparrow.string.color_string import rgb_string, GREEN


def timer(dt=0.01):
    t0 = time.time()
    q = deque(maxlen=1)
    q.append(False)
    keyboard.add_hotkey('space', lambda: q.append(not q[0]))
    current_time = 0
    while True:
        time.sleep(dt)
        ct = time.time()
        if q[0]:
            t0 = ct
        else:
            current_time += ct - t0
            print(rgb_string(f"\r{current_time:.3f} secs", color=GREEN), end='')
            t0 = ct
        if keyboard.is_pressed('q'):
            break
