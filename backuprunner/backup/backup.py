from typing import List
from pathlib import Path
import glob


class Backup:
    def __init__(self, name: str) -> None:
        self.name = name

    def run(self) -> None:
        """Run the backup"""


class PathBackup(Backup):
    def __init__(self, name: str, paths: List[str]) -> None:
        super().__init__(name)
        self.paths = paths

    def run(self) -> None:
        # TODO
        pass