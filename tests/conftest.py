from pathlib import Path

import pytest

from anki_vocab_builder.config import Config


@pytest.fixture
def test_config(tmp_path):
    """Create a test configuration with temporary directories"""
    cache_dir = tmp_path / "cache"
    config = Config(config_path=tmp_path / "config.json", cache_dir=cache_dir)
    config.config = {
        "openai_api_key": "test-api-key",
        "anki_deck_name": "Test Vocabulary",
        "anki_model_name": "Basic",
        "input_file": str(tmp_path / "words.csv"),
        "force_refresh": False,
        "cache_enabled": True,
        "cache_max_age_days": 1,
        "output_dir": str(tmp_path / "output"),
        "image_generation": True,
        "audio_generation": True,
    }
    return config


@pytest.fixture
def sample_vocab_card():
    from anki_vocab_builder.storage.models import VocabCard

    return VocabCard(
        word="test",
        quiz_question="Fill in the blank: A ____ is an assessment of knowledge.",
        meaning="An assessment of knowledge or ability",
        example_sentences=[
            "She passed the test with flying colors.",
            "This is just a test of the system.",
            "We need to test this code thoroughly.",
        ],
        pronunciation="test /tɛst/",
        image_path=Path("test_image.jpg"),
        audio_path=Path("test_audio.mp3"),
    )
