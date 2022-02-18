from pathlib import Path
import inspect


def rel_to_abs(rel_path: str, use_parent=False):
    """Return absolute path relative to the called file"""
    currentframe = inspect.currentframe()
    f = currentframe.f_back
    if use_parent:
        f = f.f_back
    current_path = Path(f.f_code.co_filename).parent
    return current_path / rel_path
