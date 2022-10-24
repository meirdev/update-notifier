import abc
import posixpath

import requests


class LatestVersion(abc.ABC):
    @abc.abstractmethod
    def get(self) -> str:
        ...


class Str(LatestVersion):
    def __init__(self, version: str) -> None:
        self.version = version

    def get(self) -> str:
        return self.version


class HttpGet(LatestVersion):
    def __init__(self, url: str) -> None:
        self.url = url

    def get(self) -> str:
        response = requests.get(self.url)
        return response.text


class PyPi(LatestVersion):
    def __init__(
        self,
        package_name: str,
        index_url: str = "https://pypi.org/pypi",
    ) -> None:
        self.package_name = package_name
        self.index_url = index_url

    def get(self) -> str:
        url = posixpath.join(self.index_url, self.package_name, "json")
        response = requests.get(url)

        return response.json().get("info", {}).get("version")
