import pytest
from pathlib import Path
from unittest.mock import patch
from anki_vocab_builder.main import main

@pytest.fixture
def setup_test_files(tmp_path):
    # Create test input CSV
    input_csv = tmp_path / "test_input.csv"
    with open(input_csv, "w") as f:
        f.write("test\nword\nexample")
    
    # Create test output directory
    output_path = tmp_path / "output"
    output_path.mkdir()
    
    return input_csv, output_path / "output.apkg"

@patch('openai.ChatCompletion.create')
@patch('openai.Image.create')
def test_main_workflow(mock_image_create, mock_chat_create, setup_test_files, test_config):
    input_csv, output_apkg = setup_test_files
    
    # Configure mocks
    mock_chat_create.return_value.choices = [
        type('obj', (), {'message': type('obj', (), {'content': 'Test content'})})()
    ]
    mock_image_create.return_value = {'data': [{'url': 'http://example.com/image.jpg'}]}
    
    # Update config with test paths
    test_config.INPUT_CSV_PATH = input_csv
    test_config.OUTPUT_ANKI_PATH = output_apkg
    
    # Run main function
    with patch('anki_vocab_builder.main.Config', return_value=test_config):
        main()
    
    # Verify output
    assert output_apkg.exists()
    assert output_apkg.stat().st_size > 0 