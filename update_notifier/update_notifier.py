import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable

from .config import Config
from .latest_version import LatestVersion
from .semver import parse_semver
from .types import SupportsLessThan
from .notification import Notification

DAY = timedelta(days=1)

CONFIG_DIR = Path("~/.config").expanduser()
CONFIG_FILE_PREFIX = "update_notifier"


class UpdateNotifier:
    def __init__(
        self,
        name: str,
        current_version: str,
        latest_version: LatestVersion,
        update_check_interval: timedelta = DAY,
        version_parser: Callable[[str], SupportsLessThan] = parse_semver,
        config_file: Path | None = None,
    ) -> None:
        self.name = name
        self.current_version = current_version
        self.latest_version = latest_version
        self.update_check_interval = update_check_interval
        self.version_parser = version_parser

        if config_file is None:
            config_file = CONFIG_DIR / f"{CONFIG_FILE_PREFIX}_{self.name}.json"

        self.config = Config(config_file)

        self.update = False
        self.update_latest_version = ""

    def check(self) -> None:
        try:
            update, last_update_check, latest_version = self.config.read()
        except:
            last_update_check = datetime.min
        else:
            if self.current_version != latest_version:
                self.update = update
                self.update_latest_version = latest_version

        if os.fork() == 0:
            now = datetime.now()

            if last_update_check + self.update_check_interval < now:
                latest_version = self.latest_version.get()

                update = self.version_parser(self.current_version) < (
                    self.version_parser(latest_version)
                )

                self.config.write(update, now, latest_version)

            sys.exit(0)

    def notify(self, notification: Notification) -> None:
        if self.update:
            notification.print(self.name, self.current_version, self.update_latest_version)


def update_notifier(
    name: str,
    current_version: str,
    latest_version: LatestVersion,
    update_check_interval: timedelta = DAY,
    version_parser: Callable[[str], SupportsLessThan] = parse_semver,
    config_file: Path | None = None,
) -> UpdateNotifier:
    obj = UpdateNotifier(
        name,
        current_version,
        latest_version,
        update_check_interval,
        version_parser,
        config_file,
    )
    obj.check()

    return obj
