from inknote.themes import (
    DEFAULT_THEME,
    get_supported_themes,
    is_valid_theme,
    validate_theme,
)


def test_default_theme_is_valid() -> None:
    assert is_valid_theme(DEFAULT_THEME)


def test_supported_themes_not_empty() -> None:
    themes = get_supported_themes()
    assert len(themes) > 0


def test_valid_theme_passes_validation() -> None:
    theme = "darkly"
    assert validate_theme(theme) == theme


def test_invalid_theme_returns_default() -> None:
    assert validate_theme("invalid_theme") == DEFAULT_THEME
