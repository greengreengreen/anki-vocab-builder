from pathlib import Path

from anki_vocab_builder.card_generator.anki_generator import AnkiGenerator
from anki_vocab_builder.config import Config
from anki_vocab_builder.enrichment.openai_client import OpenAIClient
from anki_vocab_builder.parsers.quiz_parser import QuizParser
import os


def main():
    """Process Kindle highlights and create Anki cards."""
    config = Config(config_path=Path(".anki_vocab_builder/config.json"))
        
    openai_key = os.getenv("OPENAI_API_KEY")
    openai_client = OpenAIClient(api_key=openai_key, batch_size=config.batch_size)
    quiz_parser = QuizParser()
    anki_generator = AnkiGenerator(Path(config.output_path))
    
    try:
        quiz_data = openai_client.process_kindle_highlights(config.input_path)
        quizzes = quiz_parser.parse_quiz_list(quiz_data)
        
        anki_generator.generate_deck(quizzes, "Kindle Highlights")
        print(f"Successfully created Anki deck with {len(quizzes)} cards")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
