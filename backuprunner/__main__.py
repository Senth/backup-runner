from __future__ import annotations
from backuprunner.backup.mysql_backup import MysqlBackup
from typing import List
from .backup.backup import Backup, remove_old
from .backup.path_backup import MonthlyBackup, PathBackup, WeeklyBackup
from .config import config
import backuprunner.mailer as mailer


def main():
    # Remove old backups
    remove_old()

    warnings: List[str] = []

    # MySQL backup
    if config.mysql.username and config.mysql.password:
        run_backup(MysqlBackup(), warnings)

    # Daily
    if len(config.backup.day) > 0:
        run_backup(PathBackup(config.backup.day_alias, config.backup.day), warnings)

    # Weekly
    if len(config.backup.week) > 0:
        run_backup(WeeklyBackup(config.backup.week_alias, config.backup.week), warnings)

    # Monthly
    if len(config.backup.month) > 0:
        run_backup(
            MonthlyBackup(config.backup.month_alias, config.backup.month), warnings
        )

    # Send mail
    mailer.send_warnings(warnings)
    mailer.send_if_disk_almost_full()


def run_backup(backup: Backup, warnings: List[str]):
    backup.run()

    if not backup.filepath.exists():
        warnings.append(f"Backup {backup.name} failed!  ({backup.filename})")


if __name__ == "__main__":
    main()
