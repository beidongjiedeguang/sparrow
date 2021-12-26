import random
import time

def random_idx(idx_range, exclude_idx=None):
    random.seed(time.time())
    rand_idx = random.randint(*idx_range)
    if rand_idx == exclude_idx:
        return random_idx(idx_range, exclude_idx)
    else:
        return rand_idx