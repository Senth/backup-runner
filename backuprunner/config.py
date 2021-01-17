from os import path, makedirs
from platform import system
from tempfile import gettempdir
from typing import Any, List, Union
import sys
import site
import importlib.util
import importlib.machinery
import argparse
import logging
import logging.handlers

_app_name = "backup-runner"
_config_dir = path.join("config", _app_name)
_config_file = path.join(_config_dir, "config.py")
_example_file = path.join(_config_dir, "config.example.py")

# Search for config file in sys path
_sys_config = path.join(sys.prefix, _config_file)
_user_config_file = path.join(site.getuserbase(), _config_file)
_config_file = ""
if path.exists(_sys_config):
    _config_file = _sys_config
elif path.exists(_user_config_file):
    _config_file = _user_config_file
# User hasn't configured the program yet
else:
    _sys_config_example = path.join(sys.prefix, _example_file)
    _user_config_example = path.join(site.getuserbase(), _example_file)
    if not path.exists(_sys_config_example) and not path.exists(_user_config_example):
        print(
            f"Error: no configuration found. It should be here: '{_user_config_file}'"
        )
        print("run: locate " + _example_file)
        print("This should help you find the current config location.")
        print(
            f"Otherwise you can download the config.example.py from https://github.com/Senth/{_app_name}/tree/main/config and place it in the correct location"
        )
        sys.exit(1)

    print("This seems like it's the first time you run this program.")
    print(
        f"For this program to work properly you have to configure it by editing '{_user_config_file}'"
    )
    print(
        "In the same folder there's an example file 'config.example.py' you can copy to 'config.py'."
    )
    sys.exit(0)

# Import config
_loader = importlib.machinery.SourceFileLoader("config", _user_config_file)
_spec = importlib.util.spec_from_loader(_loader.name, _loader)
_user_config: Any = importlib.util.module_from_spec(_spec)
_loader.exec_module(_user_config)


def _print_missing(variable_name):
    print(f"Missing {variable_name} variable in config file: {_user_config_file}")
    print("Please add it to you config.py again to continue")
    sys.exit(1)


class Config:
    def __init__(self, user_config):
        self._user_config = user_config

        # Default values
        self.app_name: str = _app_name
        self.logger: logging.Logger
        self.debug: bool
        self.verbose: bool
        self.backup = Backup()
        self.mysql = Mysql()
        self.warning = Warning()

        self._get_optional_variables()
        self._check_required_variables()
        self._parse_args()
        self._init_logger()

    def _parse_args(self):
        """Parse arguments from command line"""
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "--full-backup", action="store_true", help="Force a full backup run."
        )
        parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Prints out helpful messages.",
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Turn on debug messages. This automatically turns on --verbose as well.",
        )

        _args = parser.parse_args()
        self._add_args_settings(_args)

    def _add_args_settings(self, args):
        """Set additional configuration from script arguments

        Args:
            args (list): All the parsed arguments
        """
        self.backup.full = args.full_backup
        self.verbose = args.verbose
        self.debug = args.debug

        if args.debug:
            self.verbose = True

    def _get_optional_variables(self):
        """Get optional values from the config file"""
        # Backup
        try:
            self.backup.days_to_keep = _user_config.DAYS_TO_KEEP
        except AttributeError:
            pass

        try:
            self.backup.day = _user_config.DAILY_FULL
        except AttributeError:
            pass

        try:
            self.backup.day_alias = _user_config.DAILY_ALIAS
        except AttributeError:
            pass

        try:
            self.backup.week = _user_config.WEEKLY_FULL
        except AttributeError:
            pass

        try:
            self.backup.week_alias = _user_config.WEEKLY_ALIAS
        except AttributeError:
            pass

        try:
            self.backup.month = _user_config.MONTHLY_FULL
        except AttributeError:
            pass

        try:
            self.backup.month_alias = _user_config.MONTHLY_ALIAS
        except AttributeError:
            pass

        # Mysql
        try:
            self.mysql.username = _user_config.MYSQL_USERNAME
        except AttributeError:
            pass

        try:
            self.mysql.password = _user_config.MYSQL_PASSWORD
        except AttributeError:
            pass

        try:
            self.mysql.address = _user_config.MYSQL_ADDRESS
        except AttributeError:
            pass

        try:
            self.mysql.port = _user_config.MYSQL_PORT
        except AttributeError:
            pass

        # Warning
        try:
            self.warning.email_to = _user_config.EMAIL_TO
        except AttributeError:
            pass

        try:
            self.warning.email_from = _user_config.EMAIL_FROM
        except AttributeError:
            pass

        try:
            self.warning.disk_percentage = _user_config.WARN_FULL_PERCENTAGE
        except AttributeError:
            pass

    def _check_required_variables(self):
        """Check that all required variables are set in the user config file"""
        try:
            self.backup.dir = _user_config.BACKUP_DIR
        except AttributeError:
            _print_missing("BACKUP_DIR")

    def _init_logger(self):
        os = system()
        if os == "Windows":
            log_dir = path.join(gettempdir(), _app_name)
            makedirs(log_dir, exist_ok=True)
        else:
            log_dir = f"/var/log/{_app_name}/"
        log_location = path.join(log_dir, f"{_app_name}.log")

        if self.debug:
            log_level = logging.DEBUG
        elif self.verbose:
            log_level = logging.INFO
        else:
            log_level = logging.INFO

        # Set logging rotation
        timed_rotating_handler = logging.handlers.TimedRotatingFileHandler(
            log_location, when="midnight"
        )
        timed_rotating_handler.setLevel(log_level)
        timed_rotating_handler.setFormatter(
            logging.Formatter(
                "\033[1m%(asctime)s:%(levelname)s:\033[0m %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )

        # Stream output
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(log_level)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.logger.addHandler(timed_rotating_handler)
        self.logger.addHandler(stream_handler)


class Backup:
    def __init__(self) -> None:
        self.dir: str
        self.full: bool
        self.days_to_keep: int = 65
        self.day: List[str] = []
        self.day_alias: str = "daily"
        self.week: List[str] = []
        self.week_alias: str = "weekly"
        self.month: List[str] = []
        self.month_alias: str = "month"


class Mysql:
    def __init__(self) -> None:
        self.username: Union[str, None] = None
        self.password: Union[str, None] = None
        self.address: str = "localhost"
        self.port: int = 3306


class Warning:
    def __init__(self) -> None:
        self.email_to: Union[str, None] = None
        self.email_from: Union[str, None] = None
        self.disk_percentage: int = 85


global config
config = Config(_user_config)
