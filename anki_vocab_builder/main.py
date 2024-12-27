from pathlib import Path

from .card_generator.anki_generator import AnkiGenerator
from .config import Config
from .enrichment.openai_client import OpenAIClient
from .parsers.quiz_parser import QuizParser


def main():
    """Process Kindle highlights and create Anki cards."""
    config = Config(config_path=Path(".anki_vocab_builder/config.json"))
    
    if not config.openai_api_key:
        print("Error: OpenAI API key not found")
        return
        
    clippings_path = Path("input/My Clippings.txt")
    if not clippings_path.exists():
        print(f"Error: Kindle clippings file not found at {clippings_path}")
        return
        
    openai_client = OpenAIClient(config.openai_api_key)
    quiz_parser = QuizParser()
    anki_generator = AnkiGenerator(Path("output/kindle_highlights.apkg"))
    
    try:
        quiz_data = openai_client.process_kindle_highlights(clippings_path)
        quizzes = quiz_parser.parse_quiz_list(quiz_data)
        
        anki_generator.generate_deck(quizzes, "Kindle Highlights")
        print(f"Successfully created Anki deck with {len(quizzes)} cards")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
