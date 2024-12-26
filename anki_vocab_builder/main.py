from pathlib import Path

from .card_generator.anki_generator import AnkiGenerator
from .config import Config
from .enrichment.openai_client import OpenAIClient
from .storage.csv_storage import CSVStorage
from .storage.models import VocabCard


def main():
    """Process vocabulary words and create Anki cards."""
    # Initialize config
    config = Config(config_path=Path(".anki_vocab_builder/config.json"))

    # Check if OpenAI API key is configured
    if not config.openai_api_key:
        print("Error: OpenAI API key not found. Please set it in ~/.anki_vocab_builder/config.json")
        return

    # Get paths from config
    words_file = Path(config.config.get("input_file", "words.csv"))
    if not words_file.exists():
        print(f"Error: Input file {words_file} not found")
        return

    # Initialize components
    openai_client = OpenAIClient(config)
    csv_storage = CSVStorage(words_file)
    anki_generator = AnkiGenerator(config.cache_dir / "output.apkg")

    try:
        # Read words from file
        words = csv_storage.read_words()
        if not words:
            print("No words found in the input file.")
            return

        # Process each word and collect enriched data
        enriched_data_list = []
        for word in words:
            print(f"Processing word: {word}")
            try:
                enriched_data = openai_client.enrich_word(
                    word, force_refresh=config.config.get("force_refresh", False)
                )
                # Convert dictionary to VocabCard
                vocab_card = VocabCard(
                    word=enriched_data["word"],
                    quiz_question=enriched_data["quiz_question"],
                    meaning=enriched_data["meaning"],
                    example_sentences=enriched_data["example_sentences"],
                    pronunciation=enriched_data["pronunciation"],
                    image_path=Path(enriched_data["image_path"]) if enriched_data.get("image_path") else None,
                    audio_path=None  # Audio will be implemented later
                )
                enriched_data_list.append(vocab_card)
                print(f"Successfully processed: {word}")
            except Exception as e:
                print(f"Error processing word '{word}': {str(e)}")
                continue

        # Generate deck only if we have processed words
        if enriched_data_list:
            anki_generator.generate_deck(
                enriched_data_list, deck_name=config.config.get("deck_name", "Vocabulary")
            )
            print(f"Successfully created Anki deck at: {anki_generator.output_path}")
        else:
            print("No words were successfully processed. Deck generation skipped.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return


if __name__ == "__main__":
    main()
