from __future__ import annotations

from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Optional

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH

from inknote import __version__
from inknote.fileops import FileReadError, FileWriteError, read_file, write_file
from inknote.search import find_all
from inknote.settings import load_settings, save_settings
from inknote.themes import get_supported_themes, validate_theme
from inknote.updater import (
    get_latest_release,
    is_newer_version,
    open_download_page,
)


class InkNoteApp:
    """
    Main application window for InkNote.
    """

    def __init__(self, theme: str) -> None:
        self.settings = load_settings()
        self.current_file: Optional[Path] = None
        self.is_modified = False

        self.root = ttk.Window(themename=validate_theme(self.settings.theme))
        self.root.title("InkNote")
        self.root.geometry("900x600")

        self._build_ui()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._bind_shortcuts()

        self._check_for_updates()

    def _build_ui(self) -> None:
        self._build_menu()
        self._build_editor()

    def _bind_shortcuts(self) -> None:
        self.root.bind("<Control-n>", lambda e: self._new_file())
        self.root.bind("<Control-o>", lambda e: self._open_file())
        self.root.bind("<Control-s>", lambda e: self._save_file())
        self.root.bind(
            "<Control-Shift-S>", lambda e: self._save_file_as()
        )  # Fixed: Changed from <Control-S> to <Control-Shift-S>
        self.root.bind("<Control-f>", lambda e: self._open_search_dialog())
        self.root.bind("<Control-q>", lambda e: self._on_close())

    def _build_menu(self) -> None:
        menubar = ttk.Menu(self.root)

        # File menu
        file_menu = ttk.Menu(menubar, tearoff=False)

        file_menu.add_command(
            label="New",
            accelerator="Ctrl+N",
            command=self._new_file,
        )

        file_menu.add_command(
            label="Open...",
            accelerator="Ctrl+O",
            command=self._open_file,
        )

        file_menu.add_command(
            label="Save",
            accelerator="Ctrl+S",
            command=self._save_file,
        )

        file_menu.add_command(
            label="Save As...",
            accelerator="Ctrl+Shift+S",
            command=self._save_file_as,
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Exit",
            accelerator="Ctrl+Q",
            command=self.root.quit,
        )

        menubar.add_cascade(label="File", menu=file_menu)

        # Theme menu
        theme_menu = ttk.Menu(menubar, tearoff=False)

        for theme in get_supported_themes():
            theme_menu.add_command(
                label=theme,
                command=lambda t=theme: self._change_theme(t),
            )

        menubar.add_cascade(label="Theme", menu=theme_menu)

        # Search menu
        search_menu = ttk.Menu(menubar, tearoff=False)

        search_menu.add_command(
            label="Find...",
            accelerator="Ctrl+F",
            command=self._open_search_dialog,
        )

        menubar.add_cascade(label="Search", menu=search_menu)

        # Help Menu - Moved this BEFORE config(menu=menubar)
        help_menu = ttk.Menu(menubar, tearoff=False)
        help_menu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

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
        self.text_widget.bind("<<Modified>>", self._on_text_modified)
        self.text_widget.tag_configure(
            "search_highlight",
            background="yellow",
        )

    # -----------------
    # FILE OPERATIONS
    # -----------------

    def _new_file(self) -> None:
        if not self._confirm_discard_changes():
            return
        self.text_widget.delete("1.0", "end")
        self.current_file = None
        self.is_modified = False  # Moved this after setting current_file
        self._update_title()

    def _open_file(self) -> None:
        if not self._confirm_discard_changes():  # Added check for unsaved changes
            return

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
            self.is_modified = False
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
            self.is_modified = False
            self._update_title()
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
            self.is_modified = False
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
        name = self.current_file.name if self.current_file else "Untitled"
        marker = "*" if self.is_modified else ""
        self.root.title(f"InkNote {__version__} - {name}{marker}")  # Fixed extra space

    def run(self) -> None:
        self.root.mainloop()

    def _open_search_dialog(self) -> None:
        dialog = ttk.Toplevel(self.root)
        dialog.title("Find")
        dialog.geometry("300x120")
        dialog.resizable(False, False)

        ttk.Label(dialog, text="Find:").pack(pady=(10, 0))

        entry = ttk.Entry(dialog)
        entry.pack(fill="x", padx=10, pady=5)
        entry.focus()

        ignore_case_var = ttk.BooleanVar(value=False)
        ttk.Checkbutton(
            dialog,
            text="Ignore Case",
            variable=ignore_case_var,
        ).pack()

        def search_and_close() -> None:
            self._perform_search(entry.get(), ignore_case_var.get())
            dialog.destroy()

        ttk.Button(
            dialog,
            text="Search",
            command=search_and_close,
        ).pack(pady=5)

    def _perform_search(self, query: str, ignore_case: bool) -> None:
        self._clear_search_highlight()

        if not query:
            return

        content = self.text_widget.get("1.0", "end-1c")
        matches = find_all(content, query, ignore_case=ignore_case)

        for start, end in matches:
            start_index = f"1.0+{start}c"
            end_index = f"1.0+{end}c"
            self.text_widget.tag_add(
                "search_highlight",
                start_index,
                end_index,
            )

    def _clear_search_highlight(self) -> None:
        self.text_widget.tag_remove(
            "search_highlight",
            "1.0",
            "end",
        )

    def _on_text_modified(self, event: object) -> None:
        if self.text_widget.edit_modified():
            self.is_modified = True
            self._update_title()
            self.text_widget.edit_modified(False)

    def _confirm_discard_changes(self) -> bool:
        if not self.is_modified:
            return True

        result = messagebox.askyesnocancel(
            "Unsaved Changes",
            "You have unsaved changes. Save before continuing?",
        )

        if result is None:
            return False

        if result:
            self._save_file()
            return not self.is_modified

        return True

    def _on_close(self) -> None:
        if self._confirm_discard_changes():
            self.root.destroy()

    def _show_about(self) -> None:
        messagebox.showinfo(
            "About InkNote",
            f"InkNote\nVersion {__version__}\n\nA lightweight text editor.",
        )

    def _check_for_updates(self) -> None:
        latest = get_latest_release()

        if latest is None:
            return

        if is_newer_version(__version__, latest.version):
            should_open = messagebox.askyesno(
                "Update Available",
                (
                    f"A new version ({latest.version}) is available.\n\n"
                    f"Current version: {__version__}\n\n"
                    "Would you like to download it?"
                ),
            )

            if should_open:
                open_download_page(latest.url)
