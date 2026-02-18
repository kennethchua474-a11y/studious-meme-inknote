from __future__ import annotations

from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Optional

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH

from inknote.fileops import FileReadError, FileWriteError, read_file, write_file
from inknote.settings import load_settings, save_settings
from inknote.themes import get_supported_themes, validate_theme


class InkNoteApp:
    """
    Main application window for InkNote.
    """

    def __init__(self, theme: str) -> None:
        self.settings = load_settings()
        self.current_file: Optional[Path] = None

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

        file_menu.add_command(label="New", command=self._new_file)
        file_menu.add_command(label="Open...", command=self._open_file)
        file_menu.add_command(label="Save", command=self._save_file)
        file_menu.add_command(label="Save As...", command=self._save_file_as)
        file_menu.add_separator()
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

    # -----------------
    # FILE OPERATIONS
    # -----------------

    def _new_file(self) -> None:
        self.text_widget.delete("1.0", "end")
        self.current_file = None
        self._update_title()

    def _open_file(self) -> None:
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if not file_path:
            return

        try:
            content = read_file(Path(file_path))
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", content)
            self.current_file = Path(file_path)
            self._update_title()
        except FileReadError as exc:
            messagebox.showerror("Error", str(exc))

    def _save_file(self) -> None:
        if self.current_file is None:
            self._save_file_as()
            return

        try:
            content = self.text_widget.get("1.0", "end-1c")
            write_file(self.current_file, content)
        except FileWriteError as exc:
            messagebox.showerror("Error", str(exc))

    def _save_file_as(self) -> None:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )

        if not file_path:
            return

        try:
            content = self.text_widget.get("1.0", "end-1c")
            path = Path(file_path)
            write_file(path, content)
            self.current_file = path
            self._update_title()
        except FileWriteError as exc:
            messagebox.showerror("Error", str(exc))

    # -----------------
    # THEME
    # -----------------

    def _change_theme(self, theme: str) -> None:
        validated = validate_theme(theme)
        self.root.style.theme_use(validated)

        self.settings.theme = validated
        save_settings(self.settings)

    # -----------------
    # UTIL
    # -----------------

    def _update_title(self) -> None:
        if self.current_file:
            self.root.title(f"InkNote - {self.current_file.name}")
        else:
            self.root.title("InkNote")

    def run(self) -> None:
        self.root.mainloop()
