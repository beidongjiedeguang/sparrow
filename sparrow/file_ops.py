import os
import sys
import shutil
from glob import glob
from .core import broadcast
import pickle


def _rm(path):
    """remove path
    """
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            print(f'{path} is illegal.')


@broadcast
def rm(PATH):
    """ Enhanced rm, support for regular expressions """
    path_list = glob(PATH)
    for path in path_list:
        _rm(path)


def path(string: str) -> str:
    """Adaptive to different platforms """
    platform = sys.platform.lower()
    if platform in ('linux', "darwin"):
        return string.replace('\\', '/')
    elif platform in ("win", "win32"):
        return string.replace('/', '\\')
    else:
        return string


def ppath(string, file=__file__) -> str:
    """Path in package"""
    return path(os.path.join(os.path.dirname(file), string))


def save(filename, file):
    with open(filename, 'wb') as fw:
        pickle.dump(file, fw)


def load(filename):
    with open(filename, 'rb') as fi:
        file = pickle.load(fi)
    return file


def yaml_dump(filepath, data):
    from yaml import dump
    try:
        from yaml import CDumper as Dumper
    except ImportError:
        from yaml import Dumper
    with open(filepath, "w", encoding='utf-8') as fw:
        fw.write(dump(data, Dumper=Dumper))


def yaml_load(filepath):
    from yaml import load
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader
    with open(filepath, 'r', encoding="utf-8") as stream:
        #     stream = stream.read()
        content = load(stream, Loader=Loader)
    return content
