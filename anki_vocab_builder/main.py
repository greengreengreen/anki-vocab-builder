from pathlib import Path
from .config import Config
from .storage.csv_storage import CSVStorage
from .enrichment.openai_client import OpenAIEnricher
from .card_generator.anki_generator import AnkiGenerator

def main():
    # Initialize configuration
    config = Config(
        OPENAI_API_KEY="",
        INPUT_CSV_PATH=Path("test_input.csv"),
        OUTPUT_ANKI_PATH=Path("output.apkg")
    )

    # Initialize components
    csv_storage = CSVStorage(config.INPUT_CSV_PATH)
    enricher = OpenAIEnricher(config)
    anki_generator = AnkiGenerator(config.OUTPUT_ANKI_PATH)

    # Read words from CSV
    words = csv_storage.read_words()

    # Enrich words with OpenAI
    vocab_cards = []
    for word in words:
        enriched_card = enricher.enrich_word(word)
        vocab_cards.append(enriched_card)

    # Generate Anki deck
    anki_generator.generate_deck(vocab_cards)

if __name__ == "__main__":
    main()