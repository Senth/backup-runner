from tealprint import TealLevel

from .utils.config_file_args import Backups, ConfigFileArgs, Email, General, Mysql

_app_name = "backup-runner"


class Config:
    def __init__(self) -> None:
        # Default values
        self.app_name: str = _app_name
        self.level: TealLevel = TealLevel.info
        self.force_full: bool = False
        self.general = General()
        self.backups = Backups()
        self.mysql = Mysql()
        self.email = Email()

    def set_from_cli(self, args) -> None:
        """Set additional configuration from script arguments"""
        self.force_full = args.full_backup

        if args.debug:
            self.level = TealLevel.debug
        elif args.verbose:
            self.level = TealLevel.verbose

    def set_from_config_file(self, args: ConfigFileArgs) -> None:
        self.general = args.general
        self.backups = args.backups
        self.mysql = args.mysql
        self.email = args.email


config = Config()
