from pathlib import Path
import inspect


def rel_to_abs(rel_path: str, parents=0, return_str=False, strict=False):
    """Return absolute path relative to the called file
    args:
        parent: <int> The number of times `f_back` will be calledd.
    """
    currentframe = inspect.currentframe()
    f = currentframe.f_back
    if parents:
        for _ in range(parents):
            f = f.f_back
    current_path = Path(f.f_code.co_filename).parent
    pathlib_path = current_path / rel_path
    pathlib_path =  pathlib_path.resolve(strict=strict)
    if return_str:
        return str(pathlib_path)
    else:
        return pathlib_path

