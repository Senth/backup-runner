import sys
from subprocess import DEVNULL, run

from colored import attr, fg
from tealprint import TealLevel, TealPrint

from ..config import config
from .backup import Backup


class MysqlBackup(Backup):
    def __init__(self) -> None:
        super().__init__("MySQL")

    def run(self) -> None:
        # Only run if a MySQL username and password has been supplied
        if not config.mysql.username and not config.mysql.password:
            TealPrint.info(
                "Skipping MySQL backup, no username and password supplied",
                color=fg("yellow"),
            )
            return

        out = DEVNULL

        if config.level == TealLevel.debug:
            out = sys.stdout

        TealPrint.info("Backing up MySQL", color=attr("bold"))

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

        TealPrint.info("✔ MySQL backup complete!")

    @property
    def extension(self) -> str:
        return "sql"
