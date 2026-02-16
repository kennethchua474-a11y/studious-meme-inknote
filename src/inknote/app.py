from __future__ import annotations

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH

from inknote.settings import load_settings, save_settings
from inknote.themes import get_supported_themes, validate_theme


class InkNoteApp:
    """
    Main application window for InkNote.
    """

    def __init__(self, theme: str) -> None:
        self.settings = load_settings()

        self.root = ttk.Window(themename=validate_theme(self.settings.theme))
        self.root.title("InkNote")
        self.root.geometry("900x600")

        self._build_ui()

    def _build_ui(self) -> None:
        self._build_menu()
        self._build_editor()

    def _build_menu(self) -> None:
        menubar = ttk.Menu(self.root)

        # File menu
        file_menu = ttk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Theme menu
        theme_menu = ttk.Menu(menubar, tearoff=False)

        for theme in get_supported_themes():
            theme_menu.add_command(
                label=theme,
                command=lambda t=theme: self._change_theme(t),
            )

        menubar.add_cascade(label="Theme", menu=theme_menu)

        self.root.config(menu=menubar)

    def _build_editor(self) -> None:
        frame = ttk.Frame(self.root)
        frame.pack(fill=BOTH, expand=True)

        self.text_widget = ttk.Text(
            frame,
            wrap="word",
            undo=True,
        )
        self.text_widget.pack(fill=BOTH, expand=True)

    def _change_theme(self, theme: str) -> None:
        validated = validate_theme(theme)
        self.root.style.theme_use(validated)

        self.settings.theme = validated
        save_settings(self.settings)

    def run(self) -> None:
        self.root.mainloop()
