from pathlib import Path
from anki_vocab_builder.parsers.quiz_parser import QuizParser
from anki_vocab_builder.card_generator.anki_generator import AnkiGenerator

# Define where you want to save the deck
output_path = Path("./my_deck.apkg")

# Create sample data (same as in the test)
sample_data = [
    {
        "type": "type_in",
        "question": "The _____ walked to the store.",
        "answer": "person",
        "source": "Test Book (Author)",
        "meaning": "A human being",
        "examples": ["The person was friendly.", "Many people attended the event."]
    },
    {
        "type": "qa",
        "question": "What is the capital of France?",
        "answer": "Paris",
        "source": "History Book (Author)",
        "quotes": ["The capital of France is Paris.", "Paris is the capital of France."]
    }
]

# Parse and generate the deck
parser = QuizParser()
quizzes = parser.parse_quiz_list(sample_data)
generator = AnkiGenerator(output_path)
generator.generate_deck(quizzes, "My Test Deck")

print(f"Deck created at: {output_path.absolute()}") 