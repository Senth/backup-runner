from .backup import Backup
from subprocess import DEVNULL, run
from ..config import config
from ..logger import LogColors, Logger
import sys


class MysqlBackup(Backup):
    def __init__(self) -> None:
        super().__init__("MySQL")

    def run(self) -> None:
        # Only run if a MySQL username and password has been supplied
        if not config.mysql.username and not config.mysql.password:
            Logger.info(
                "Skipping MySQL backup, no username and password supplied",
                LogColors.header,
            )
            return

        out = DEVNULL

        if config.debug:
            out = sys.stdout

        Logger.info("Backing up MySQL", LogColors.header)

        args = [
            "mysqldump",
            "-u",
            str(config.mysql.username),
            f"--password={config.mysql.password}",
            "-r",
            str(self.filepath),
            "--all-databases",
        ]

        run(
            args,
            stdout=out,
        )

        Logger.info("MySQL backup complete!")

    @property
    def extension(self) -> str:
        return "sql"