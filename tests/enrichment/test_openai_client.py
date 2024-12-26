import json
import time
from unittest.mock import Mock, patch

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
