import os

from .file_ops import yaml_load, yaml_dump
from .string import string_add


class VersionControl:
    def __init__(self,
                 pkgname,
                 pkgdir,
                 version=None,
                 filename="version-config.yaml",
                 ):

        self.config = None
        self._pkgname = pkgname
        self._config_path = os.path.join(pkgdir, filename)
        if version is None:
            try:
                self.get_config()
            except:
                print(f"{filename} was not exist, created now.")
                self.gen_config('0.0.0')
        else:
            self.gen_config(version)

    def gen_config(self, version="0.0.0"):
        config = {"name": self._pkgname, "version": version}
        self.config = config
        yaml_dump(self._config_path, config)

    def get_config(self):
        config = yaml_load(self._config_path)
        self.config = config
        return config

    def set_version(self, version):
        self.config['version'] = version

    def save_config(self):
        yaml_dump(self._config_path, self.config)

    def update_version(self, version_step=1):
        self.config['version'] = string_add(self.config["version"], version_step)
        yaml_dump(self._config_path, self.config)

    def clean_config_file(self):
        os.remove(self._config_path)

    def update_readme_require(self, readme_path="README.md",
                      requirements_path="requirements.txt",
                      license="GNU_GPL--v3",
                      author="kunyuan",
                      replace_flag=19*'-'):
        with open(readme_path, 'r', encoding='UTF-8') as fr:
            readme = fr.read()
        with open(requirements_path, 'r', encoding="utf-8") as fr:
           requirements = fr.read().strip("\n")
        replace_begin = f"""# {self._pkgname}
[![image](https://img.shields.io/badge/Pypi-{self.config['version']}-green.svg)](https://pypi.org/project/{self._pkgname})
[![image](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![image](https://img.shields.io/badge/{license}-blue.svg)](LICENSE)
[![image](https://img.shields.io/badge/author-{author}-orange.svg?style=flat-square&logo=appveyor)](https://github.com/beidongjiedeguang)

## Requirements
```bash
{requirements}
```

"""
        readme_list = readme.split(replace_flag)
        readme_list[0] = replace_begin
        new_readme = replace_flag.join(readme_list)

        with open('README.md', 'w', encoding='UTF-8') as fo:
            fo.write(new_readme)

