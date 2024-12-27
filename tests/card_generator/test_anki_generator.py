from pathlib import Path
import pytest
from anki_vocab_builder.card_generator.anki_generator import AnkiGenerator
from anki_vocab_builder.storage.models import TypeInQuiz, QAQuiz

@pytest.fixture
def output_path(tmp_path):
    return tmp_path / "test_deck.apkg"

@pytest.fixture
def generator(output_path):
    return AnkiGenerator(output_path)

@pytest.fixture
def sample_type_in_quiz():
    return TypeInQuiz(
        question="Test question?",
        answer="Test answer",
        source="Test Source",
        meaning="Test meaning",
        examples=["Example 1", "Example 2"]
    )

@pytest.fixture
def sample_qa_quiz():
    return QAQuiz(
        question="Test question?",
        answer="Test answer",
        source="Test Source",
        quotes=["Quote 1", "Quote 2"],
        key_terms=[{"term": "Test", "definition": "Definition"}],
        related_concepts=["Concept 1", "Concept 2"]
    )

@pytest.mark.parametrize("quiz_class,expected_fields", [
    (TypeInQuiz, ["Question", "Answer", "Source", "Meaning", "Examples", 
                  "Synonyms", "Antonyms", "WordFamily"]),
    (QAQuiz, ["Question", "Answer", "Source", "Quotes", "KeyTerms", "RelatedConcepts"])
])
def test_model_fields(generator, quiz_class, expected_fields):
    quiz = quiz_class(
        question="Test question?",
        answer="Test answer",
        source="Test Source"
    )
    model = generator._get_or_create_model(quiz)
    
    actual_fields = [field["name"] for field in model.fields]
    assert actual_fields == expected_fields

def test_generate_deck_creates_file(generator, sample_type_in_quiz, output_path):
    generator.generate_deck([sample_type_in_quiz], "Test Deck")
    assert output_path.exists()

def test_generate_mixed_deck(generator, sample_type_in_quiz, sample_qa_quiz, output_path):
    generator.generate_deck([sample_type_in_quiz, sample_qa_quiz], "Mixed Deck")
    assert output_path.exists()
