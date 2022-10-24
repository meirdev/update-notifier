import re
from typing import NamedTuple, cast

# https://semver.org/

REGEX_STRING = r"""
^
    (?P<major>0|[1-9]\d*)
    \.
    (?P<minor>0|[1-9]\d*)
    \.
    (?P<patch>0|[1-9]\d*)
    (?:
        -
        (?P<prerelease>
            (?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)
            (?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*
        )
    )?
    (?:
        \+
        (?P<buildmetadata>
            [0-9a-zA-Z-]+
            (?:\.[0-9a-zA-Z-]+)*
        )
    )?
$
"""

REGEX = re.compile(REGEX_STRING, re.VERBOSE)


class Semver(NamedTuple):
    major: int
    minor: int
    patch: int
    pre_release: str | None = None
    build: str | None = None

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Semver):
            raise NotImplementedError

        # 2.
        for s, o in [
            (self.major, other.major),
            (self.minor, other.minor),
            (self.patch, other.patch),
        ]:
            if s != o:
                return s < o

        # 3.
        if self.pre_release is not None and other.pre_release is None:
            return True

        if self.pre_release is None and other.pre_release is not None:
            return False

        if self.pre_release is None and other.pre_release is None:
            return False

        # 4.
        s = self.pre_release.split(".")
        o = other.pre_release.split(".")

        for si, oi in zip(s, o):
            if si != oi:
                # 4.1
                if si.isdigit() and oi.isdigit():
                    si, oi = int(si), int(oi)
                # 4.2-3
                return si < oi

        # 4.4
        return len(s) < len(o)

    def __gt__(self, other) -> bool:
        return other < self

    def __eq__(self, other) -> bool:
        s = (self.major, self.minor, self.patch, self.pre_release)
        o = (other.major, other.minor, other.patch, other.pre_release)
        return s == o

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __ge__(self, other) -> bool:
        return other < self or self == other


def parse_semver(semver: str) -> Semver:
    if match := re.match(REGEX, semver):
        return Semver(
            major=int(match["major"]),
            minor=int(match["minor"]),
            patch=int(match["patch"]),
            pre_release=match["prerelease"],
            build=match["buildmetadata"],
        )

    raise ValueError(f"Invalid semver: {semver}")
