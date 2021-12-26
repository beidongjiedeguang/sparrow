from pathlib import Path
import inspect


def rel_to_abs(rel_path: str):
    """Return absolute path relative to the called file """
    currentframe = inspect.currentframe()
    f = currentframe.f_back
    current_path = Path(f.f_code.co_filename).parent
    return current_path / rel_path


if __name__ == "__main__":
    print(rel_to_abs("../emmm"))
