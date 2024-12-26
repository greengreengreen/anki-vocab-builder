import pytest
from unittest.mock import Mock, patch
from anki_vocab_builder.enrichment.openai_client import OpenAIEnricher

@pytest.fixture
def mock_openai_responses():
    return {
        'quiz': Mock(choices=[Mock(message=Mock(content="Fill in the blank: A ____ is an assessment."))]),
        'content': Mock(choices=[Mock(message=Mock(content="1. An assessment of knowledge\n- She took the test.\n- This is a test.\n- Testing is important.\n/tɛst/"))]),
        'image': {'data': [{'url': 'http://example.com/image.jpg'}]}
    }

@pytest.fixture
def enricher(test_config):
    return OpenAIEnricher(test_config)

@patch('openai.ChatCompletion.create')
@patch('openai.Image.create')
def test_enrich_word(mock_image_create, mock_chat_create, enricher, mock_openai_responses):
    # Setup mocks
    mock_chat_create.side_effect = [
        mock_openai_responses['quiz'],
        mock_openai_responses['content']
    ]
    mock_image_create.return_value = mock_openai_responses['image']
    
    # Test enrichment
    card = enricher.enrich_word("test")
    
    assert card.word == "test"
    assert card.quiz_question == "Fill in the blank: A ____ is an assessment."
    assert "assessment" in card.meaning.lower()
    assert len(card.example_sentences) == 3
    assert all(s.startswith('-') for s in card.example_sentences)
    assert card.pronunciation == "/tɛst/"

def test_parse_content(enricher):
    content = """An assessment of knowledge
- First example
- Second example
- Third example
/tɛst/"""
    
    meaning, examples, pronunciation = enricher._parse_content(content)
    
    assert "assessment" in meaning.lower()
    assert len(examples) == 3
    assert pronunciation == "/tɛst/" 