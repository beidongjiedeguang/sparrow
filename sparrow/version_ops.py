import os
from .file_ops import yaml_load, yaml_dump
from .string import string_add


class VersionControl:
    def __init__(self,
                 pkgname,
                 filename="version-config.yaml",
                 version="0.0.0"):
        self.config = None
        self.pkgname = pkgname
        self.filename = filename
        if not os.path.exists(filename):
            self.gen_config(pkgname, version, filename)
        else:
            self.config = yaml_load(filename)

    def gen_config(self, name, version, filename="version-config.yaml"):
        config = {"name": name, "version": version}
        self.config = config
        yaml_dump(filename, config)

    def get_config(self, filename="version-config.yaml"):
        config = yaml_load(filename)
        self.config = config
        return config

    def set_version(self, version):
        self.config['version'] = version

    def update_version(self, version_step=1):
        self.config['version'] = string_add(self.config["version"], version_step)
        yaml_dump(self.filename, self.config)

    def clean_config_file(self):
        os.remove(self.filename)
