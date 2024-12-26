import pytest
from pathlib import Path
from anki_vocab_builder.config import Config

@pytest.fixture
def test_config():
    return Config(
        OPENAI_API_KEY="test-api-key",
        INPUT_CSV_PATH=Path("test_input.csv"),
        OUTPUT_ANKI_PATH=Path("test_output.apkg"),
        AUDIO_OUTPUT_DIR=Path("test_audio_files")
    )

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
            "We need to test this code thoroughly."
        ],
        pronunciation="test /tɛst/",
        image_path=Path("test_image.jpg"),
        audio_path=Path("test_audio.mp3")
    ) 