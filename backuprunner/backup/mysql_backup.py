from .backup import Backup
from subprocess import DEVNULL, run
from ..config import config
import sys


class MysqlBackup(Backup):
    def __init__(self) -> None:
        super().__init__("MySQL")

    def run(self) -> None:
        # Only run if a MySQL username and password has been supplied
        if not config.mysql.username and not config.mysql.password:
            config.logger.info(
                "Skipping MySQL backup, no username and password supplied"
            )
            return

        out = DEVNULL

        if config.debug:
            out = sys.stdout

        config.logger.info("Backing up MySQL")
        config.logger.debug(
            f"Username: {config.mysql.username}, password: {config.mysql.password}"
        )

        run(
            [
                "mysqldump",
                "-u",
                str(config.mysql.username),
                "-p",
                str(config.mysql.password),
                "-r",
                self.filepath,
                "--all-databases",
            ],
            stdout=out,
        )

    @property
    def extension(self) -> str:
        return "sql"