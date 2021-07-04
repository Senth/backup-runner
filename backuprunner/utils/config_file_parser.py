import configparser
from pathlib import Path
from shutil import copy
from site import getuserbase
from typing import Any

from tealprint import TealPrint

from ..config import config
from .config_file_args import ConfigFileArgs


class ConfigFileParser:
    def __init__(self) -> None:
        self.path = Path.home().joinpath(f".{config.app_name}.cfg")

    def get_args(self) -> ConfigFileArgs:
        args = ConfigFileArgs()

        if not self.path.exists():
            TealPrint.error(f"Could not find config file {self.path}. Please add!", exit=True)
            return args

        config = configparser.ConfigParser()
        config.read(self.path)

        if "general" in config:
            general = config["general"]
            ConfigFileParser._set_str(
                args.general,
                general,
                "backup_location",
                "days_to_keep",
            )

        if "backups" in config:
            backups = config["backups"]
            ConfigFileParser._set_str_list(
                args.backups,
                backups,
                "daily",
                "weekly",
                "monthly",
            )
            ConfigFileParser._set_str(
                args.backups,
                backups,
                "daily_alias",
                "weekly_alias",
                "monthly_alias",
            )

        if "mysql" in config:
            mysql = config["mysql"]
            ConfigFileParser._set_str(
                args.mysql,
                mysql,
                "username",
                "password",
                "address",
            )
            ConfigFileParser._set_int(
                args.mysql,
                mysql,
                "port",
            )

        if "email" in config:
            email = config["email"]
            ConfigFileParser._set_str(
                args.email,
                email,
                "to",
                "from",
            )
            ConfigFileParser._set_int(
                args.email,
                email,
                "disk_percentage",
            )

        return args

    @staticmethod
    def _set_str(args: Any, section: configparser.SectionProxy, *varnames: str) -> None:
        for varname in varnames:
            default = getattr(args, varname)
            value = section.get(varname, fallback=default)
            setattr(args, varname, value)

    @staticmethod
    def _set_str_list(args: Any, section: configparser.SectionProxy, *varnames: str) -> None:
        for varname in varnames:
            values = getattr(args, varname)
            value = section.get(varname, fallback="")
            if value != "":
                values = value.split("\n")
            setattr(args, varname, values)

    @staticmethod
    def _set_int(args: Any, section: configparser.SectionProxy, *varnames: str) -> None:
        for varname in varnames:
            default = getattr(args, varname)
            value = section.getint(varname, fallback=default)
            setattr(args, varname, value)

    @staticmethod
    def _read_from_config(config: configparser.SectionProxy, varname: str) -> Any:
        varname = varname.lower()
        if varname in config:
            return config[varname]
        return None

    def _check_required(self, args: ConfigFileArgs) -> None:
        if len(args.general.backup_location) == 0:
            self._print_missing("General", "backup_location")

    def _print_missing(self, section: str, varname: str) -> None:
        TealPrint.error(
            f"Missing {varname} under section {section}. " + f"Please add it to your configuration file {self.path}",
            exit=True,
        )

    def create_if_not_exists(self) -> None:
        if self.path.exists():
            return

        # Copy file from config location to home
        example_name = f"{config.app_name}-example.cfg"
        example_path = Path(getuserbase()).joinpath("config", example_name)

        if not example_path.exists():
            return

        copy(example_path, self.path)
