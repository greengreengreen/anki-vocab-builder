from pathlib import Path

import pytest

from anki_vocab_builder.config import Config


@pytest.fixture
def test_config(tmp_path):
    """Create a test configuration with temporary directories"""
    config = Config(config_path=tmp_path / "config.json")
    config.config = {
        "anki_deck_name": "Test Deck",
        "anki_model_name": "Basic",
        "input_path": str(tmp_path / "input/kindle/My Clippings.txt"),
        "output_path": str(tmp_path / "output/kindle_highlights.apkg"),
        "batch_size": 5,
        "force_refresh": True,
        "cache_max_age_days": 1,
        "gpt_model": "gpt-4o"
    }
    return config
