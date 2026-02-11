from __future__ import annotations

from pathlib import Path


class FileReadError(Exception):
    """Raised when a file cannot be read."""


class FileWriteError(Exception):
    """Raised when a file cannot be written."""


def read_file(path: Path) -> str:
    """
    Reads a UTF-8 text file and normalizes line endings to '\\n'.
    Raises FileReadError on failure.
    """
    try:
        content = path.read_text(encoding="utf-8")
        return content.replace("\r\n", "\n")
    except OSError as exc:
        raise FileReadError(f"Failed to read file: {path}") from exc


def write_file(path: Path, content: str) -> None:
    """
    Writes content to a file using UTF-8 encoding.
    Converts interal '\\n' to Windows CRLF before writing.
    Raises FileWriteError on failure.
    """
    try:
        # Convert internal LF to CRLF for Windows consistency
        normalized = content.replace("\n", "\r\n")
        path.write_text(normalized, encoding="utf-8")
    except OSError as exc:
        raise FileWriteError(f"Failed to write file: {path}") from exc
