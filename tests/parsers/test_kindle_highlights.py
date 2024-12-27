from datetime import datetime
from pathlib import Path

import pytest

from anki_vocab_builder.parsers.kindle_highlights import (
    format_highlight,
    parse_date,
    parse_kindle_clippings,
)


@pytest.fixture
def sample_clippings_file(tmp_path):
    content = """Mythical Man-Month, The (Brooks Jr., Frederick P.)
- Your Highlight on page 45 | Location 484-485 | Added on Saturday, September 21, 2024 9:41:08 PM

The data showed no correlation whatsoever between experience and performance.
==========
How to Live (Sivers, Derek)
- Your Highlight on page 63 | Added on Saturday, September 21, 2024 11:09:23 PM

If you haven't decided what to master, pick anything that scares you.
=========="""

    file_path = tmp_path / "My Clippings.txt"
    file_path.write_text(content)
    return file_path


def test_parse_date():
    date_str = "Saturday, September 21, 2024 9:41:08 PM"
    result = parse_date(date_str)
    assert result == "2024-09-21"


def test_parse_date_invalid():
    date_str = "Invalid Date Format"
    result = parse_date(date_str)
    assert result == ""


def test_parse_kindle_clippings(sample_clippings_file):
    highlights = parse_kindle_clippings(sample_clippings_file)

    assert len(highlights) == 2
    highlight, source, date = highlights[0]

    assert (
        highlight == "The data showed no correlation whatsoever between experience and performance."
    )
    assert source == "Mythical Man-Month, The (Brooks Jr., Frederick P.)"
    assert date == "2024-09-21"


def test_format_highlight():
    highlight = "Test highlight"
    source = "Test Book (Author)"
    date = "24-09-21"

    formatted = format_highlight(highlight, source, date)
    assert formatted == "Highlight (24-09-21):\nTest highlight\nSource: Test Book (Author)"


def test_parse_kindle_clippings_empty_file(tmp_path):
    empty_file = tmp_path / "Empty.txt"
    empty_file.write_text("")
    highlights = parse_kindle_clippings(empty_file)
    assert highlights == []


def test_parse_kindle_clippings_invalid_format(tmp_path):
    invalid_file = tmp_path / "Invalid.txt"
    invalid_file.write_text("Invalid format content")
    highlights = parse_kindle_clippings(invalid_file)
    assert highlights == []
