from pathlib import Path
from typing import List
from .backup import Backup, BackupParts
from glob import glob
from tarfile import TarFile


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