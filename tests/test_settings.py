from pathlib import Path

import pytest
from inknote.settings import (
    DEFAULT_THEME,
    Settings,
    SettingsError,
    get_settings_path,
    load_settings,
    save_settings,
)


@pytest.fixture
def fake_appdata(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setenv("APPDATA", str(tmp_path))
    return tmp_path


def test_default_settings_when_file_missing(fake_appdata: Path) -> None:
    settings = load_settings()
    assert settings.theme == DEFAULT_THEME


def test_save_and_load_settings(fake_appdata: Path) -> None:
    settings = Settings(theme="darkly")
    save_settings(settings)

    loaded = load_settings()

    assert loaded.theme == "darkly"


def test_corrupted_json_returns_defaults(fake_appdata: Path) -> None:
    path = get_settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text("Invalid JSON", encoding="utf-8")

    with pytest.raises(SettingsError):
        load_settings()


def test_invalid_theme_in_file_returns_default(fake_appdata: Path) -> None:
    path = get_settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        '{"theme": "invalid_theme"}',
        encoding="utf-8",
    )

    settings = load_settings()

    assert settings.theme == DEFAULT_THEME
