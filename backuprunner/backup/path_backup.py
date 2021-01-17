from pathlib import Path
from typing import List
from .backup import Backup, BackupParts
from glob import glob
import tarfile
from ..logger import Logger, LogColors
import backuprunner.date_helper as date_helper


class PathBackup(Backup):
    def __init__(self, name: str, paths: List[str]) -> None:
        super().__init__(name)
        self.paths = paths
        self.tar = tarfile.open(self.filepath, "w:gz")

    def run(self) -> None:
        """Add files to tar"""
        Logger.info(f"Backing up {self.name}", LogColors.header)

        # Full backup
        if self.part == BackupParts.full:
            Logger.info(f"Full backup")
            for path_glob in self.paths:
                Logger.info(f"-> {path_glob}")
                for path in glob(path_glob):
                    Logger.debug(f"  -> {path}", LogColors.added)
                    self.tar.add(path)

        # Diff backup
        else:
            Logger.info("Diff backup")
            for path_glob in self.paths:
                Logger.info(f"-> {path_glob}")
                for path in glob(path_glob):
                    self._find_diff_files(Path(path), 1)

    def _find_diff_files(self, path: Path, level: int):
        log_padding = "  " * level
        # File/Dir has changed
        try:
            if path.is_symlink() or (
                not path.is_dir() and self.is_modified_within_diff(path)
            ):
                Logger.debug(f"{log_padding}-> {path}", LogColors.added)
                self.tar.add(path)
            # Check children
            else:
                Logger.debug(f"{log_padding}-> {path}")
                if not path.is_symlink():
                    for child in path.glob("*"):
                        self._find_diff_files(child, level + 1)
                    for child in path.glob(".*"):
                        self._find_diff_files(child, level + 1)
        except FileNotFoundError:
            pass

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