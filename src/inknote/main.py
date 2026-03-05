from __future__ import annotations

import sys

from inknote.app import InkNoteApp
from inknote.themes import DEFAULT_THEME


def main() -> None:
    # Future-proof hook for frozen apps
    if getattr(sys, "frozen", False):
        # Running as bundled executable
        pass

    app = InkNoteApp(theme=DEFAULT_THEME)
    app.run()


if __name__ == "__main__":
    main()
