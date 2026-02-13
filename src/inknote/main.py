from __future__ import annotations

from inknote.app import InkNoteApp
from inknote.themes import DEFAULT_THEME


def main() -> None:
    app = InkNoteApp(theme=DEFAULT_THEME)
    app.run()


if __name__ == "__main__":
    main()
