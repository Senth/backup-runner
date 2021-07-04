from typing import List, Optional


class ConfigFileArgs:
    def __init__(self) -> None:
        self.general = General()
        self.backups = Backups()
        self.mysql = Mysql()
        self.email = Email()


class General:
    def __init__(self) -> None:
        self.backup_location: str = ""
        self.days_to_keep: int = 65


class Backups:
    def __init__(self) -> None:
        self.daily: List[str] = []
        self.daily_alias: str = "daily"
        self.weekly: List[str] = []
        self.weekly_alias: str = "weekly"
        self.monthly: List[str] = []
        self.monthly_alias: str = "monthly"


class Mysql:
    def __init__(self) -> None:
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.address: str = "localhost"
        self.port: int = 3306


class Email:
    def __init__(self) -> None:
        self.to_address: Optional[str] = None
        self.from_address: Optional[str] = None
        self.disk_percentage: int = 85
