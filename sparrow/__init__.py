from .file_ops import yaml_load, yaml_dump, ppath, save, load, rm
from .decorator import runtime
from .color_str import rgb_string

_version_config = yaml_load(ppath("version-config.yaml"))
__version__= _version_config['version']
print(f"{_version_config['name']} version: {__version__}")
