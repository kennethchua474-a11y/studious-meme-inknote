from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Final

from inknote.themes import DEFAULT_THEME, validate_theme

APP_NAME: Final[str] = "InkNote"
SETTINGS_FILENAME: Final[str] = "settings.json"


@dataclass(slots=True)
class Settings:
    theme: str = DEFAULT_THEME


class SettingsError(Exception):
    """Raised when settings cannot be loaded or saved."""


def get_appdata_dir() -> Path:
    """
    Returns platfor-specific application data directory.
    Windows: %APPDATA%/InkNote
    Linux/macOS (dev): ~/.config/InkNote
    """
    appdata_env = os.getenv("APPDATA")

    if appdata_env:
        base = Path(appdata_env)
    if os.name == "nt":
        base = Path(os.environ["APPDATA"])
    else:
        base = Path.home() / ".config"

    path = base / APP_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_settings_path() -> Path:
    """
    Returns the full path to the settings json file.
    """
    return get_appdata_dir() / SETTINGS_FILENAME


def load_settings() -> Settings:
    """
    The function loads settings from disk.
    If file does not exist or is corrupted, it returns default settings.
    """
    path = get_settings_path()

    if not path.exists():
        settings = Settings()
        save_settings(settings)
        return settings

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        theme = validate_theme(raw.get("theme", DEFAULT_THEME))
        return Settings(theme=theme)
    except (OSError, json.JSONDecodeError) as exc:
        raise SettingsError("Failed to load settings") from exc


def save_settings(settings: Settings) -> None:
    """
    Saves settings to disk.
    """
    path = get_settings_path()

    try:
        path.write_text(json.dumps(asdict(settings), indent=4), encoding="utf-8")
    except OSError as exc:
        raise SettingsError("Failed to save settings") from exc
