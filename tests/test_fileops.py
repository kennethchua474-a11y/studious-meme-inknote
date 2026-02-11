from pathlib import Path

import pytest
from inknote.fileops import FileReadError, FileWriteError, read_file, write_file


def test_write_and_read_file(tmp_path: Path) -> None:
    file_path = tmp_path / "test.txt"
    content = "Line1\nLine2\n"

    write_file(file_path, content)
    loaded = read_file(file_path)

    assert loaded == content


def test_read_nonexistent_file_raises() -> None:
    with pytest.raises(FileReadError):
        read_file(Path("nonexistent_file.txt"))


def test_write_invalid_path_raises(tmp_path: Path) -> None:
    invalid_path = tmp_path / "nonexistent_dir" / "file.txt"

    with pytest.raises(FileWriteError):
        write_file(invalid_path, "data")
