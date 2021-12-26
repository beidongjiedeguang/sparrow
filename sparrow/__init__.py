from .file_ops import yaml_load, yaml_dump, ppath, save, load, rm
from .decorator import benchmark
from .color.color_str import rgb_string
from .functions.core import clamp


_version_config = yaml_load(ppath("version-config.yaml", __file__))
__version__= _version_config['version']
print(f"{rgb_string(_version_config['name'], color='#34A853')} version: {rgb_string(__version__, color='#C9E8FF')}")
