from .version_ops import yaml_load
from .file_ops import ppath


_version_config = yaml_load(ppath("version-config.yaml"))
__version__= _version_config['version']
print(f"{_version_config['name']} version is: {__version__}")
