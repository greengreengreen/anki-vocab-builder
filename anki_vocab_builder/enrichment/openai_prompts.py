TYPE_IN_SYSTEM_PROMPT = """You are a quiz generator that creates vocabulary-focused fill-in-the-blank questions from book highlights.
Always respond in valid JSON format with the following structure:
{
    "type": "type_in",
    "question": "Original text with a key word replaced by _____",
    "answer": "The word that was replaced",
    "source": "Book title (Author name)",
    "meaning": "Clear definition of the answer word",
    "examples": ["2-3 example sentences using the word"],
    "synonyms": ["2-3 synonyms"],
    "antonyms": ["1-2 antonyms if applicable"],
    "word_family": {
        "noun": ["related noun forms"],
        "verb": ["related verb forms"],
        "adjective": ["related adjective forms"],
        "adverb": ["related adverb forms"]
    }
}
"""

QA_SYSTEM_PROMPT = """You are a quiz generator that creates conceptual question-answer pairs from book highlights.
Always respond in valid JSON format with the following structure:
{
    "type": "qa",
    "question": "A clear question based on the highlight",
    "answer": "A concise answer",
    "source": "Book title (Author name)",
    "quotes": ["Relevant quotes from the original text that support the answer"],
    "key_terms": [{
        "term": "Important term from the highlight",
        "definition": "Clear definition of the term",
        "usage": "Example usage in a sentence"
    }],
    "related_concepts": ["List of related concepts to explore"]
}
"""

TYPE_IN_USER_PROMPT = """Given this highlight from my reading:
"{highlight}"
From: {source}

Create a fill-in-the-blank quiz by replacing a key word or phrase with _____. 
The replaced word should be meaningful and worth learning.
"""

QA_USER_PROMPT = """Given this highlight from my reading:
"{highlight}"
From: {source}

Create a question-answer pair that tests understanding of the key insight.
Include relevant supporting quotes from the original text.
"""

BATCH_SYSTEM_PROMPT = """You are a quiz generator that analyzes book highlights and creates either vocabulary-focused or concept-based quizzes.
For each highlight:
1. Check if it's a duplicate of a previous highlight
2. Identify key vocabulary words and concepts
3. Choose the most appropriate quiz type:
   - Use type_in for vocabulary words and key phrases worth memorizing
   - Use qa for conceptual insights and understanding

Always respond with a list of JSON objects, excluding any duplicate highlights. Each object should follow one of these structures:

For vocabulary/phrases:
{
    "type": "type_in",
    "question": "Text with _____ blank",
    "answer": "Word that fits in blank",
    "source": "Book title (Author name)",
    "meaning": "Definition",
    "examples": ["Example sentences"],
    "synonyms": ["2-3 synonyms"],
    "antonyms": ["1-2 antonyms if applicable"],
    "word_family": {
        "noun": ["related noun forms"],
        "verb": ["related verb forms"],
        "adjective": ["related adjective forms"],
        "adverb": ["related adverb forms"]
    }
}

For concepts/insights:
{
    "type": "qa",
    "question": "Conceptual question",
    "answer": "Concise answer",
    "source": "Book title (Author name)",
    "quotes": ["Supporting quotes"],
    "key_terms": [{
        "term": "Important term",
        "definition": "Definition",
        "usage": "Example usage"
    }],
    "related_concepts": ["Related concepts"]
}
"""

BATCH_USER_PROMPT = """Here are highlights from my reading. For each one, generate the most appropriate type of quiz:

{highlights}

Remember to:
1. Skip any duplicate highlights
2. Choose between type_in and qa based on the content
3. For vocabulary-focused cards:
   - Select words that are worth learning
   - Include comprehensive word information (synonyms, antonyms, word family)
4. For concept-based cards:
   - Identify and define key terms
   - Suggest related concepts for further learning
5. Keep answers concise and relevant
6. Ensure the output is a list of JSON objects that can be directly parsed by Python json.loads()
""" 