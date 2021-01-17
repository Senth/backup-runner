from datetime import datetime
from pathlib import Path
from enum import Enum

from ..config import config
import backuprunner.date_helper as date_helper


class BackupParts(Enum):
    full = ("full",)
    day_diff = "day-diff"
    week_diff = "week-diff"


class Backup:
    def __init__(self, name: str) -> None:
        self.name = name
        self._diff_start: datetime
        self._diff_end: datetime
        self._calculate_part_diffs()

    def run(self) -> None:
        """Run the backup"""

    def is_modified_within_diff(self, path: Path) -> bool:
        modified_time = date_helper.get_modified_datetime(path)
        return self._diff_start <= modified_time and modified_time <= self._diff_end
        pass

    @property
    def filename(self) -> str:
        """Filename to use for the backup"""
        return f"{self.name} {date_helper.yesterday_str()} {self.part.value}.{self.extension}"

    @property
    def filepath(self) -> Path:
        """Full filepath to the backup"""
        return Path(config.backup.dir).joinpath(self.filename)

    @property
    def part(self) -> BackupParts:
        return BackupParts.full

    @property
    def extension(self) -> str:
        return ""

    def _calculate_part_diffs(self) -> None:
        # Day diff
        if self.part == BackupParts.day_diff:
            self._diff_start = date_helper.yesterday()

        # Weekly diff
        elif self.part == BackupParts.week_diff:
            self._diff_start = date_helper.last_week()

        else:
            self._diff_start = date_helper.today()

        self._diff_end = date_helper.today()
