import pytest
from pathlib import Path
from anki_vocab_builder.card_generator.anki_generator import AnkiGenerator

@pytest.fixture
def anki_generator(tmp_path):
    return AnkiGenerator(tmp_path / "test_output.apkg")

def test_generate_deck(anki_generator, sample_vocab_card, tmp_path):
    # Test deck generation with a single card
    output_path = tmp_path / "test_output.apkg"
    anki_generator.output_path = output_path
    
    anki_generator.generate_deck([sample_vocab_card])
    
    assert output_path.exists()
    assert output_path.stat().st_size > 0

def test_generate_empty_deck(anki_generator, tmp_path):
    # Test generating deck with no cards
    output_path = tmp_path / "empty_deck.apkg"
    anki_generator.output_path = output_path
    
    anki_generator.generate_deck([])
    
    assert output_path.exists()

def test_deck_model_fields(anki_generator):
    # Test that the model has all required fields
    expected_fields = {'Word', 'Quiz', 'Meaning', 'Examples', 'Pronunciation', 'Image', 'Audio'}
    model_fields = {field['name'] for field in anki_generator.model.fields}
    
    assert model_fields == expected_fields 