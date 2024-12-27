import json
import time
from unittest.mock import Mock, patch
from pathlib import Path

import pytest
import requests

from anki_vocab_builder.enrichment.openai_client import OpenAIClient


@pytest.fixture
def client(test_config, tmp_path):
    with patch("openai.OpenAI") as mock_openai:
        test_config.cache_dir = tmp_path
        client = OpenAIClient(test_config)
        client.cache_file.write_text("{}")
        client.cache = {}
        return client


@patch("openai.OpenAI")
@patch("requests.get")
def test_enrich_word(mock_requests_get, mock_openai, client):
    # Setup mock OpenAI client
    mock_client = Mock()
    mock_openai.return_value = mock_client
    client.client = mock_client  # Replace the client directly

    # Mock responses
    mock_client.chat.completions.create.side_effect = [
        Mock(choices=[Mock(message=Mock(content="Fill in the blank: A ____ is an assessment."))]),
        Mock(
            choices=[
                Mock(
                    message=Mock(
                        content="1. An assessment of knowledge\n- Example 1\n- Example 2\n/test/"
                    )
                )
            ]
        ),
    ]

    mock_client.images.generate.return_value = Mock(data=[Mock(url="http://example.com/image.jpg")])

    # Mock image download
    mock_requests_get.return_value = Mock(content=b"fake_image_data", raise_for_status=Mock())

    # Test enrichment
    result = client.enrich_word("test", force_refresh=True)

    # Verify the result
    assert result["word"] == "test"
    assert "assessment" in result["quiz_question"]
    assert "image_url" in result
    assert "image_path" in result


@pytest.fixture
def sample_highlights():
    return [
        ("If you haven't decided what to master, pick anything that scares you, fascinates you, or infuriates you.",
         "How to Live (Sivers, Derek)",
         "24-09-21"),
        ("The layman's understanding of quantum mechanics is quite different from reality.",
         "Some Physics Book (Author)",
         "24-09-21")
    ]


@patch("openai.OpenAI")
def test_process_kindle_highlights(mock_openai, client, sample_highlights):
    # Setup mock OpenAI client
    mock_client = Mock()
    mock_openai.return_value = mock_client
    
    # Mock response with both quiz types
    mock_response = Mock()
    mock_response.choices[0].message.content = json.dumps([
        {
            "type": "qa",
            "question": "How do you decide what to master?",
            "answer": "Pick anything that scares you, fascinates you, or infuriates you.",
            "source": "How to Live (Sivers, Derek)",
            "quotes": ["If you haven't decided what to master, pick anything that scares you, fascinates you, or infuriates you."]
        },
        {
            "type": "type_in",
            "question": "The _____'s understanding of quantum mechanics is quite different from reality.",
            "answer": "layman",
            "source": "Some Physics Book (Author)",
            "meaning": "A person without professional or specialized knowledge in a particular subject",
            "examples": ["He explained the complex theory in layman's terms."]
        }
    ])
    mock_client.chat.completions.create.return_value = mock_response
    
    # Test highlight processing
    with patch("anki_vocab_builder.parsers.kindle_highlights.parse_kindle_clippings", return_value=sample_highlights):
        result = client.process_kindle_highlights(Path("dummy/path"))
    
    assert len(result) == 2
    assert result[0]["type"] == "qa"
    assert result[1]["type"] == "type_in"
