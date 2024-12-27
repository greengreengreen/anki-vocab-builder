import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from anki_vocab_builder.config import Config
from anki_vocab_builder.main import main


@pytest.fixture
def setup_test_environment(tmp_path):
    # Create test directories
    input_dir = tmp_path / "input" / "kindle"
    input_dir.mkdir(parents=True)
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True)

    # Create test clippings file
    clippings_file = input_dir / "My Clippings.txt"
    clippings_file.write_text(
        """The Martian (Weir, Andy)
- Your Highlight on page 45 | Added on Saturday, September 21, 2024 9:41:08 PM

I guess I should explain how Mars missions work, for any layman who may be reading this.
=========="""
    )

    # Create config file
    config_file = tmp_path / "config.json"
    config = {
        "anki_deck_name": "Test Deck",
        "input_path": str(clippings_file),
        "output_path": str(output_dir / "kindle_highlights.apkg"),
        "batch_size": 5,
    }
    config_file.write_text(json.dumps(config))

    # Return actual Config object instead of Mock
    return Config(config_path=config_file)


@patch("openai.OpenAI")
def test_main_workflow(mock_openai, setup_test_environment, tmp_path):
    config = setup_test_environment

    # Mock OpenAI response
    mock_client = Mock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.return_value = Mock(
        choices=[
            Mock(
                message=Mock(
                    content=json.dumps(
                        [
                            {
                                "type": "type_in",
                                "question": "I guess I should explain how Mars missions work, for any _____ who may be reading this.",
                                "answer": "layman",
                                "source": "The Martian (Weir, Andy)",
                                "meaning": "A person without professional knowledge",
                                "examples": ["He explained it in layman's terms"],
                            }
                        ]
                    )
                )
            )
        ]
    )

    # Run main function
    with patch("anki_vocab_builder.main.Config", return_value=config):
        main()

    # Verify output file was created
    output_file = Path(config.config["output_path"])
    assert output_file.exists()
