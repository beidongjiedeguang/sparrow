import os
import sys
import shutil
from glob import glob
from sparrow.path import rel_to_abs
from deprecated import deprecated
import pickle
from .core import broadcast


@broadcast
def rm(PATH):
    """Enhanced rm, support for regular expressions"""

    def _rm(path):
        """remove path"""
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            else:
                print(f"{path} is illegal.")

    path_list = glob(PATH)
    for path in path_list:
        _rm(path)


def path(string: str) -> str:
    """Adaptive to different platforms"""
    platform = sys.platform.lower()
    if platform in ("linux", "darwin"):
        return string.replace("\\", "/")
    elif platform in ("win", "win32"):
        return string.replace("/", "\\")
    else:
        return string


def save(filename, file):
    with open(filename, "wb") as fw:
        pickle.dump(file, fw)


def load(filename):
    with open(filename, "rb") as fi:
        file = pickle.load(fi)
    return file


def yaml_dump(filepath, data, rel_path=False):
    abs_path = rel_to_abs(filepath, parents=1) if rel_path else filepath
    from yaml import dump

    try:
        from yaml import CDumper as Dumper
    except ImportError:
        from yaml import Dumper
    with open(abs_path, "w", encoding="utf-8") as fw:
        fw.write(dump(data, Dumper=Dumper, allow_unicode=True, indent=4))


def yaml_load(filepath, rel_path=False):
    abs_path = rel_to_abs(filepath, parents=1) if rel_path else filepath
    from yaml import load

    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader
    with open(abs_path, "r", encoding="utf-8") as stream:
        #     stream = stream.read()
        content = load(stream, Loader=Loader)
    return content
