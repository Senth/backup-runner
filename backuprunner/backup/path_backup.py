from pathlib import Path
from typing import List
from .backup import Backup, BackupParts
from glob import glob
from tarfile import TarFile

import backuprunner.date_helper as date_helper


class PathBackup(Backup):
    def __init__(self, name: str, paths: List[str]) -> None:
        super().__init__(name)
        self.paths = paths
        self.tar: TarFile = TarFile(self.filepath, mode="w:gz")

    def run(self) -> None:
        """Add files to tar"""
        # Full backup
        if self.part == BackupParts.full:
            for path_glob in self.paths:
                for path in glob(path_glob):
                    self.tar.add(path)

        # Diff backup
        else:
            for path_name in self.paths:
                for path in glob(path_name):
                    self._find_diff_files(Path(path))

    def _find_diff_files(self, path: Path):
        # File/Dir has changed
        if self.is_modified_within_diff(path):
            self.tar.add(path)
        # Check children
        else:
            for child in path.glob("*"):
                self._find_diff_files(child)
            for child in path.glob(".*"):
                self._find_diff_files(child)

    @property
    def extension(self) -> str:
        return "tgz"


class WeeklyBackup(PathBackup):
    def __init__(self, name: str, paths: List[str]) -> None:
        super().__init__(name, paths)

    def _get_part(self) -> BackupParts:
        if date_helper.is_today_monday():
            return BackupParts.full
        else:
            return BackupParts.day_diff


class MonthlyBackup(PathBackup):
    def __init__(self, name: str, paths: List[str]) -> None:
        super().__init__(name, paths)

    def _get_part(self) -> BackupParts:
        day = date_helper.day_of_month()

        if day == 1:
            return BackupParts.full
        elif (day - 1) % 7 == 0:
            return BackupParts.week_diff
        else:
            return BackupParts.day_diff