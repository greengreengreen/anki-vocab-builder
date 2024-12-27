import pytest
from anki_vocab_builder.parsers.quiz_parser import QuizParser
from anki_vocab_builder.storage.models import TypeInQuiz, QAQuiz


@pytest.fixture
def type_in_quiz_data():
    return {
        "type": "type_in",
        "question": "The _____ walked to the store.",
        "answer": "person",
        "source": "Test Book (Author)",
        "meaning": "A human being",
        "examples": ["The person was friendly.", "Many people attended the event."],
        "synonyms": ["individual", "human", "being"],
        "antonyms": ["group", "crowd"],
        "word_family": {
            "noun": ["person", "persons", "people"],
            "adjective": ["personal"],
            "adverb": ["personally"]
        }
    }


@pytest.fixture
def qa_quiz_data():
    return {
        "type": "qa",
        "question": "What is the main theme of the book?",
        "answer": "The importance of persistence",
        "source": "Test Book (Author)",
        "quotes": ["Success comes from persistence.", "Never give up."],
        "key_terms": [{
            "term": "persistence",
            "definition": "Continuing despite difficulties",
            "usage": "His persistence led to success"
        }],
        "related_concepts": ["determination", "grit", "resilience"]
    }


def test_parse_type_in_quiz(type_in_quiz_data):
    quiz = QuizParser.parse_quiz(type_in_quiz_data)
    
    assert isinstance(quiz, TypeInQuiz)
    assert quiz.question == type_in_quiz_data["question"]
    assert quiz.answer == type_in_quiz_data["answer"]
    assert quiz.source == type_in_quiz_data["source"]
    assert quiz.meaning == type_in_quiz_data["meaning"]
    assert quiz.examples == type_in_quiz_data["examples"]
    assert quiz.synonyms == type_in_quiz_data["synonyms"]
    assert quiz.antonyms == type_in_quiz_data["antonyms"]
    assert quiz.word_family == type_in_quiz_data["word_family"]


def test_parse_qa_quiz(qa_quiz_data):
    quiz = QuizParser.parse_quiz(qa_quiz_data)
    
    assert isinstance(quiz, QAQuiz)
    assert quiz.question == qa_quiz_data["question"]
    assert quiz.answer == qa_quiz_data["answer"]
    assert quiz.source == qa_quiz_data["source"]
    assert quiz.quotes == qa_quiz_data["quotes"]
    assert quiz.key_terms == qa_quiz_data["key_terms"]
    assert quiz.related_concepts == qa_quiz_data["related_concepts"]


def test_parse_quiz_with_missing_optional_fields():
    data = {
        "type": "type_in",
        "question": "Test question?",
        "answer": "test",
        "source": "Test Book"
    }
    
    quiz = QuizParser.parse_quiz(data)
    
    assert isinstance(quiz, TypeInQuiz)
    assert quiz.meaning is None
    assert quiz.examples == []
    assert quiz.synonyms == []
    assert quiz.antonyms == []
    assert quiz.word_family == {}


def test_parse_quiz_with_invalid_type():
    data = {
        "type": "invalid_type",
        "question": "Test question?",
        "answer": "test",
        "source": "Test Book"
    }
    
    with pytest.raises(ValueError) as exc_info:
        QuizParser.parse_quiz(data)
    
    assert "Unknown quiz type: invalid_type" in str(exc_info.value)


def test_parse_quiz_list(type_in_quiz_data, qa_quiz_data):
    quiz_data = [type_in_quiz_data, qa_quiz_data]
    quizzes = QuizParser.parse_quiz_list(quiz_data)
    
    assert len(quizzes) == 2
    assert isinstance(quizzes[0], TypeInQuiz)
    assert isinstance(quizzes[1], QAQuiz)


def test_parse_quiz_list_empty():
    quizzes = QuizParser.parse_quiz_list([])
    assert len(quizzes) == 0


def test_parse_quiz_missing_required_fields():
    data = {
        "type": "type_in",
        "question": "Test question?"
        # Missing required 'answer' and 'source' fields
    }
    
    with pytest.raises(KeyError):
        QuizParser.parse_quiz(data) 