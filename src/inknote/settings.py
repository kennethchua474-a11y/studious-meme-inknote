from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

APP_NAME = "InkNote"
SETTINGS_FILENAME = "settings.json"


@dataclass(slots=True)
class Settings:
    theme: str = "flatly"
    show_line_numbers: bool = True
    show_status_bar: bool = True
    window_width: int = 1000
    window_height: int = 700


def get_appdata_dir() -> Path:
    """
    Returns the Windows %APPDATA% directory.
    Raise RuntimeError if APPDATA is not set.
    """
    appdata = os.getenv("APPDATA")
    if not appdata:
        raise RuntimeError("APPDATA environment variable is not set.")
    return Path(appdata)


def get_settings_path() -> Path:
    """
    Returns the full path to the settings json file.
    """
    base_dir = get_appdata_dir() / APP_NAME
    return base_dir / SETTINGS_FILENAME


def ensure_settings_directory() -> None:
    """
    Creates the application settings directory if it does not exist.
    """
    settings_dir = get_settings_path().parent
    settings_dir.mkdir(parents=True, exist_ok=True)


def load_settings() -> Settings:
    """
    The function loads settings from disk.
    If file does not exist or is corrupted, it returns default settings.
    """
    path = get_settings_path()

    if not path.exists():
        return Settings()

    try:
        data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        return Settings(**data)
    except (json.JSONDecodeError, TypeError, OSError):
        return Settings()


def save_settings(settings: Settings) -> bool:
    """
    Saves settings to disk.
    Returns True if successful, False otherwise.
    """
    try:
        ensure_settings_directory()
        path = get_settings_path()
        path.write_text(
            json.dumps(asdict(settings), indent=4),
            encoding="utf-8",
        )
        return True
    except (OSError, TypeError):
        # Log the error in a real application
        return False
