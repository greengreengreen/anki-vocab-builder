from pathlib import Path

import pytest
from unittest.mock import Mock, patch
import genanki

from anki_vocab_builder.card_generator.anki_generator import AnkiGenerator
from anki_vocab_builder.storage.models import TypeInQuiz


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
        source="Test Source"
    )


@pytest.mark.parametrize("quiz_class,expected_fields", [
    (TypeInQuiz, ["Question", "Answer", "Source", "Meaning", "Examples"]),
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
