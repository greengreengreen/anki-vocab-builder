from pathlib import Path

import pytest

from anki_vocab_builder.card_generator.anki_generator import AnkiGenerator


@pytest.fixture
def anki_generator(test_config, tmp_path):
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "test_output.apkg"
    # Ensure parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return AnkiGenerator(output_path)


def test_generate_deck(anki_generator, sample_vocab_card):
    # Test deck generation with a single card
    deck_name = "Test Deck"
    anki_generator.generate_deck([sample_vocab_card], deck_name=deck_name)

    assert anki_generator.output_path.exists()
    assert anki_generator.output_path.stat().st_size > 0


def test_generate_empty_deck(anki_generator):
    # Test generating deck with no cards
    anki_generator.generate_deck([])
    assert anki_generator.output_path.exists()


def test_deck_model_fields(anki_generator):
    # Test that the model has all required fields
    expected_fields = {"Word", "Quiz", "Meaning", "Examples", "Pronunciation", "Image", "Audio"}
    model_fields = {field["name"] for field in anki_generator.model.fields}
    assert model_fields == expected_fields
