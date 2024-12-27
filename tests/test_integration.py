import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from anki_vocab_builder.main import main


@pytest.fixture
def setup_test_environment(tmp_path):
    # Create test config and input directory
    input_dir = tmp_path / "input"
    input_dir.mkdir(parents=True)
    clippings_file = input_dir / "My Clippings.txt"
    
    config = {
        "openai_api_key": "test_key",
        "kindle_clippings": str(clippings_file),
        "deck_name": "Test Deck",
        "cache_dir": str(tmp_path / "cache")
    }
    
    # Create test clippings file
    clippings_file.write_text('''Mythical Man-Month, The (Brooks Jr., Frederick P.)
- Your Highlight on page 45 | Location 484-485 | Added on Saturday, September 21, 2024 9:41:08 PM

The data showed no correlation whatsoever between experience and performance.
==========''')
    
    return Mock(
        config=config,
        openai_api_key="test_key",
        cache_dir=tmp_path / "cache"
    )


@patch("openai.OpenAI")
def test_main_workflow(mock_openai, setup_test_environment, capsys):
    config = setup_test_environment
    
    # Mock OpenAI response
    mock_client = Mock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.return_value = Mock(
        choices=[Mock(message=Mock(content=json.dumps([{
            "type": "qa",
            "question": "Test question?",
            "answer": "Test answer",
            "source": "Test Book",
            "quotes": ["Test quote"]
        }])))]
    )
    
    # Run main function
    with patch("anki_vocab_builder.main.Config", return_value=config):
        main()
        
    captured = capsys.readouterr()
    assert "Successfully created Anki deck" in captured.out


def test_main_no_api_key(capsys):
    """Test main function with missing API key"""
    with patch("anki_vocab_builder.main.Config") as mock_config:
        mock_config.return_value.openai_api_key = ""
        main()

    captured = capsys.readouterr()
    assert "Error: OpenAI API key not found" in captured.out
