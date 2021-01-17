from typing import List
from .config import config
from subprocess import Popen, PIPE
import psutil

_header = f"""to: {config.warning.email_to}
from: {config.warning.email_from}
content-type: text/html
"""


def _send_mail(mail: str) -> None:
    if config.warning.email_to and config.warning.email_from:
        p = Popen(["sendmail", "-t"], stdin=PIPE)
        p.communicate(input=mail.encode(encoding="utf-8"))


def send_if_disk_almost_full() -> None:
    disk = psutil.disk_usage(config.backup.dir)

    mail = _header
    mail += f"""subject: Backup disk almost full! {disk.percent}% USED
    <strong>Used (%):</strong> {disk.percent}%<br />
    <strong>Size:</strong> {disk.total}<br />
    <strong>Free:</strong> {disk.free}<br />
    <strong>Used:</strong> {disk.used}<br />
    """

    _send_mail(mail)


def send_warnings(warnings: List["str"]) -> None:
    if len(warnings) > 0:
        mail = _header
        mail += f"subject: {len(warnings)} backups failed!\n"
        for warning in warnings:
            mail += warning + "\n"

        _send_mail(mail)
