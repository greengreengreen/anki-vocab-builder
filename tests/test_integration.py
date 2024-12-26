import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from anki_vocab_builder.main import main


@pytest.fixture
def setup_test_environment(tmp_path, test_config):
    """Set up test environment with necessary files"""
    # Create input file
    input_file = Path(test_config.config["input_file"])
    input_file.parent.mkdir(parents=True, exist_ok=True)
    with open(input_file, "w") as f:
        f.write("test\nword\nexample")

    # Create output directory
    output_dir = Path(test_config.config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    # Set up cache directory
    test_config.cache_dir = tmp_path / "cache"
    test_config.cache_dir.mkdir(parents=True, exist_ok=True)

    return test_config


@patch("openai.OpenAI")
def test_main_workflow(mock_openai, setup_test_environment, capsys):
    config = setup_test_environment

    # Configure mock OpenAI client
    mock_client = Mock()
    mock_openai.return_value = mock_client

    # Mock chat completions with proper response structure
    mock_client.chat.completions.create.return_value = Mock(
        choices=[
            Mock(
                message=Mock(
                    content=json.dumps(
                        {
                            "quiz_question": "Test quiz",
                            "meaning": "Test meaning",
                            "example_sentences": ["Example 1"],
                            "pronunciation": "/test/",
                        }
                    )
                )
            )
        ]
    )

    # Mock image generation
    mock_client.images.generate.return_value = Mock(data=[Mock(url="http://example.com/image.jpg")])

    # Run main function
    with patch("anki_vocab_builder.main.Config", return_value=config):
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(content=b"fake_data", raise_for_status=Mock())
            # Create a list to store enriched data
            enriched_data = []

            # Mock OpenAIClient.enrich_word to return proper data structure
            with patch(
                "anki_vocab_builder.enrichment.openai_client.OpenAIClient.enrich_word"
            ) as mock_enrich:
                mock_enrich.return_value = {
                    "word": "test",
                    "quiz_question": "Test quiz",
                    "meaning": "Test meaning",
                    "example_sentences": ["Example 1"],
                    "pronunciation": "/test/",
                    "image_path": "test_image.jpg",
                }
                main()

    # Check output
    captured = capsys.readouterr()
    assert "Processing word: test" in captured.out
    assert "Successfully processed: test" in captured.out


def test_main_no_api_key(capsys):
    """Test main function with missing API key"""
    with patch("anki_vocab_builder.main.Config") as mock_config:
        mock_config.return_value.openai_api_key = ""
        main()

    captured = capsys.readouterr()
    assert "Error: OpenAI API key not found" in captured.out
