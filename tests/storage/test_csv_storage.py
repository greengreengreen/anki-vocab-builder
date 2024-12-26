# tests/storage/test_csv_storage.py
from pathlib import Path

import pytest

from anki_vocab_builder.storage.csv_storage import CSVStorage


def test_read_words(tmp_path):
    # Create a temporary CSV file
    csv_path = tmp_path / "test_words.csv"
    with open(csv_path, "w") as f:
        f.write("hello\nworld\ntest")

    # Test reading words
    storage = CSVStorage(csv_path)
    words = storage.read_words()

    assert len(words) == 3
    assert words == ["hello", "world", "test"]


def test_read_empty_csv(tmp_path):
    # Test with empty CSV
    csv_path = tmp_path / "empty.csv"
    csv_path.touch()

    storage = CSVStorage(csv_path)
    words = storage.read_words()

    assert len(words) == 0


def test_read_nonexistent_file():
    # Test with non-existent file
    storage = CSVStorage(Path("nonexistent.csv"))
    with pytest.raises(FileNotFoundError):
        storage.read_words()
