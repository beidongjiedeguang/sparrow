from sparrow.path import rel_to_abs
from sparrow import yaml_load
import os


def test_rel_to_abs():
    assert os.path.exists(rel_to_abs("test_path.py"))
    assert os.path.exists(rel_to_abs("../sparrow"))
    assert os.path.exists(rel_to_abs("../sparrow/__init__.py"))
