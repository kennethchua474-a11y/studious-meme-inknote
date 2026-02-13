from __future__ import annotations

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH

from inknote.themes import validate_theme


class InkNoteApp:
    """
    Main application window for InkNote.
    """

    def __init__(self, theme: str) -> None:
        validated_theme = validate_theme(theme)
        self.root = ttk.Window(themename=validated_theme)
        self.root.title("InkNote")
        self.root.geometry("900x600")

        self._build_ui()

    def _build_ui(self) -> None:
        self._build_menu()
        self._build_editor()

    def _build_menu(self) -> None:
        menubar = ttk.Menu(self.root)

        file_menu = ttk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        menubar.add_cascade(label="File", menu=file_menu)

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

    def run(self) -> None:
        self.root.mainloop()
