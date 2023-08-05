import pathlib
import sys
import yaml

from xdg import BaseDirectory


class configize():
    def __init__(self, **kwargs):
        if not sys.platform.startswith("linux"):
            raise NotImplementedError("This library is only designed for Linux")

        basedir = pathlib.Path(
            kwargs.get(
                "Path",
                BaseDirectory.xdg_config_home
            )
        )
        name = kwargs.get("Name")
        self.path = None
        for path in (
            "{0}.yaml".format(name),
            "{0}.yml".format(name),
            "{0}/{0}.yaml".format(name),
            "{0}/{0}.yml".format(name),
            "{0}/config.yaml".format(name),
            "{0}/config.yml".format(name),
          ):
            full_path = basedir.joinpath(path)
            if full_path.is_file():
                self.path = full_path

        if self.path is None:
            raise ValueError("No config file found")

        with open(self.path, "r") as conf:
            self.config = yaml.load(conf, Loader=yaml.SafeLoader)
