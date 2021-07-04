import configparser
from pathlib import Path
from shutil import copy
from site import getuserbase
from typing import Any

from ..config import config
from .config_file_args import ConfigFileArgs


class ConfigFileParser:
    def __init__(self) -> None:
        self.path = Path.home().joinpath(f".{config.app_name}.cfg")

    def get_args(self) -> ConfigFileArgs:
        args = ConfigFileArgs()

        if not self.path.exists():
            return args

        config = configparser.ConfigParser()
        config.read(self.path)

        # TODO add configuration variables
        # if "General" in config:
        #     args.port = ConfigFileParser._read_from_config(config["General"], "Port")

        return args

    @staticmethod
    def _read_from_config(config: configparser.SectionProxy, varname: str) -> Any:
        varname = varname.lower()
        if varname in config:
            return config[varname]
        return None

    def create_if_not_exists(self) -> None:
        if self.path.exists():
            return

        # Copy file from config location to home
        example_name = f"{config.app_name}-example.cfg"
        example_path = Path(getuserbase()).joinpath("config", example_name)

        if not example_path.exists():
            return

        copy(example_path, self.path)
