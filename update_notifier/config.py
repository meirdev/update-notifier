import json
from datetime import datetime
from pathlib import Path
from typing import NamedTuple


class Data(NamedTuple):
    update: bool
    last_update_check: datetime
    latest_version: str


class Config:
    def __init__(self, file: Path) -> None:
        self.file = file

    def read(self) -> Data:
        with open(self.file) as fp:
            config = json.load(fp)
            return Data(
                config["update"],
                datetime.fromisoformat(config["last_update_check"]),
                config["latest_version"],
            )

    def write(
        self,
        update: bool,
        last_update_check: datetime,
        latest_version: str,
    ) -> None:
        with open(self.file, "w") as fp:
            config = {
                "update": update,
                "last_update_check": last_update_check.isoformat(),
                "latest_version": latest_version,
            }
            json.dump(config, fp)
