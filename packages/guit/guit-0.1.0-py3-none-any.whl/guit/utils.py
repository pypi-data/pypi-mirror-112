import webbrowser
from typing import Dict, Mapping, Optional

from parse import parse
from sh import git

from .constants import GIT_URL_PATTERNS


def rchop(s: str, suffix: str) -> str:
    # Source: https://stackoverflow.com/a/3663505
    if suffix and s.endswith(suffix):
        return s[: -len(suffix)]
    return s


# More info:
# - https://amoffat.github.io/sh/sections/subcommands.html
# - https://amoffat.github.io/sh/sections/command_class.html#runningcommand-class
def get_current_branch() -> str:
    # RunningCommand objects behave like strings.
    # git rev-parse --abbrev-ref HEAD
    return git("rev-parse", "--abbrev-ref", "HEAD").strip()


def get_remote_url() -> str:
    # There are SSH and HTTPS URLs.
    # More info: https://docs.github.com/en/get-started/getting-started-with-git/about-remote-repositories  # noqa

    # Alternatives:
    # - git remote --verbose (https://github.com/cfarvidson/git-open)
    # - git remote show origin (https://stackoverflow.com/a/4089452)
    # - git config --get remote.origin.url
    return git("config", "--get", "remote.origin.url").strip()


def open_url(url: str) -> None:
    webbrowser.open(url)


def make_https_url(params: Mapping[str, str]) -> str:
    return rchop(GIT_URL_PATTERNS["https"].format(**params), ".git")


def parse_remote_url(url: str) -> Optional[Dict[str, str]]:
    # Short-circuiting loop.
    # More info: https://realpython.com/python-return-statement/#short-circuiting-loops
    for pattern in GIT_URL_PATTERNS.values():
        params = parse(pattern, url)

        if params is not None:
            return params.named

    # Returning None explicitly.
    # More info: https://realpython.com/python-return-statement/#returning-none-explicitly  # noqa
    return None
