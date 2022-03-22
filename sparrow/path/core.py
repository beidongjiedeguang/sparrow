from pathlib import Path
import inspect


def rel_to_abs(rel_path: str, parents=0):
    """Return absolute path relative to the called file"""
    currentframe = inspect.currentframe()
    f = currentframe.f_back
    if parents:
        for _ in range(parents):
            f = f.f_back
    current_path = Path(f.f_code.co_filename).parent
    return current_path / rel_path
