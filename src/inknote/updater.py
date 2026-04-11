import webbrowser
from dataclasses import dataclass

import requests

GITHUB_API_RELEASES = "https://api.github.com/repos/kennethchua474-a11y/studious-meme-inknote/releases/latest"


@dataclass(frozen=True)
class UpdateInfo:
    version: str
    url: str


def get_latest_release() -> UpdateInfo | None:
    try:
        response = requests.get(GITHUB_API_RELEASES, timeout=5)
        response.raise_for_status()

        data = response.json()
        version = data["tag_name"].lstrip("v")
        url = data["html_url"]

        return UpdateInfo(version=version, url=url)

    except requests.RequestException:
        return None


def open_download_page(url: str) -> None:
    webbrowser.open(url)


def is_newer_version(current: str, latest: str) -> bool:
    return tuple(map(int, latest.split("."))) > tuple(map(int, current.split(".")))
