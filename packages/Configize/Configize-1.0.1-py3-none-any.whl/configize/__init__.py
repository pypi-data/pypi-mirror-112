import pathlib
import sys
import yaml

from typing import Tuple as Tuple, Optional as Optional
from xdg import BaseDirectory as BaseDirectory # type: ignore


class configize():
    def __init__(self, **kwargs: str) -> None:

        if not sys.platform.startswith("linux"):
            raise NotImplementedError("This library is only designed for Linux")

        try:
            name: Optional[str] = kwargs.get("Name")
        except AttributeError as e:
            raise ValueError("No name provided") from e

        basedir: pathlib.Path = pathlib.Path(
            kwargs.get(
                "Path",
                BaseDirectory.xdg_config_home
            )
        )
        self.search_paths: Tuple[str, str, str, str, str, str] = (
            "{0}.yaml".format(name),
            "{0}.yml".format(name),
            "{0}/{0}.yaml".format(name),
            "{0}/{0}.yml".format(name),
            "{0}/config.yaml".format(name),
            "{0}/config.yml".format(name),
        )
        self.path: pathlib.Path

        for path in self.search_paths:
            full_path: pathlib.Path = basedir.joinpath(path)
            if full_path.is_file():
                self.path = full_path

        try:
            getattr(self, "path")
        except AttributeError as e:
            raise ValueError("No config file found") from e

        with open(self.path, "r") as conf:
            self.config: dict = yaml.load(conf, Loader=yaml.SafeLoader)
