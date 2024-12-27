from pathlib import Path

from anki_vocab_builder.card_generator.anki_generator import AnkiGenerator
from anki_vocab_builder.config import Config
from anki_vocab_builder.enrichment.openai_client import OpenAIClient
from anki_vocab_builder.parsers.quiz_parser import QuizParser


def main():
    """Process Kindle highlights and create Anki cards."""
    config = Config(config_path=Path(".anki_vocab_builder/config.json"))
    
    if not config.openai_api_key:
        print("Error: OpenAI API key not found")
        return
        
    clippings_path = Path(".anki_vocab_builder/input/kindle/My Clippings.txt")
    if not clippings_path.exists():
        print(f"Error: Kindle clippings file not found at {clippings_path}")
        return
        
    openai_client = OpenAIClient(config.openai_api_key)
    quiz_parser = QuizParser()
    anki_generator = AnkiGenerator(Path(".anki_vocab_builder/output/kindle_highlights.apkg"))
    
    try:
        quiz_data = openai_client.process_kindle_highlights(clippings_path)
        quizzes = quiz_parser.parse_quiz_list(quiz_data)
        
        anki_generator.generate_deck(quizzes, "Kindle Highlights")
        print(f"Successfully created Anki deck with {len(quizzes)} cards")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
