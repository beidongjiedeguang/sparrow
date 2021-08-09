from .file_ops import yaml_load, yaml_dump, ppath, save, load, rm
from .decorator import runtime
from .color_str import rgb_string


_version_config = yaml_load(ppath("version-config.yaml"))
__version__= _version_config['version']
print(f"{rgb_string(_version_config['name'], color='#34A853')} version: {rgb_string(__version__, color='#C9E8FF')}")
