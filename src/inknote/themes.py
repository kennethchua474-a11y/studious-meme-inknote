from __future__ import annotations

from typing import List

DEFAULT_THEME = "flatly"

# Curated theme list for Windows app
SUPPORTED_THEMES: List[str] = [
    "flatly",
    "cosmo",
    "litera",
    "minty",
    "lumen",
    "sandstone",
    "yeti",
    "pulse",
    "united",
    "darkly",
    "superhero",
    "cyborg",
]


class InvalidThemeError(ValueError):
    """Raised when an unsupported theme is requested."""


def get_supported_themes() -> List[str]:
    """
    Returns the list of supported ttkbootstrap themes.
    """
    return list(SUPPORTED_THEMES)


def is_valid_theme(theme: str) -> bool:
    """
    Returns True if the theme is supported.
    """
    return theme in SUPPORTED_THEMES


def validate_theme(theme: str) -> str:
    """
    Returns the theme if valid, otherwise returns DEFAULT_THEME
    """
    if is_valid_theme(theme):
        return theme
    return DEFAULT_THEME
