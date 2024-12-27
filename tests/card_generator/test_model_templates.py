import pytest

from anki_vocab_builder.card_generator.model_templates import ModelTemplates
from anki_vocab_builder.storage.models import QAQuiz, TypeInQuiz


@pytest.fixture
def sample_type_in_quiz():
    return TypeInQuiz(
        question="From Book: The Martian\nI guess I should explain how Mars missions work, for any _____ who may be reading this.",
        answer="layman",
        source="The Martian (Weir, Andy)",
        meaning="A person without professional knowledge in a particular subject",
        examples=["He explained the complex procedure in layman's terms."],
        synonyms=["novice", "amateur", "beginner"],
        antonyms=["expert", "professional"],
        word_family={"noun": ["layman", "laymen"], "adjective": ["lay"], "adverb": ["laically"]},
    )


def test_type_in_template():
    template = ModelTemplates.get_template(TypeInQuiz)

    # Test front template
    assert "{{type:Answer}}" in template["qfmt"]
    assert "{{Source}}" in template["qfmt"]
    assert "type-prompt" in template["qfmt"]

    # Test back template
    assert "{{Meaning}}" in template["afmt"]
    assert "{{Examples}}" in template["afmt"]
    assert "{{Synonyms}}" in template["afmt"]
    assert "{{Antonyms}}" in template["afmt"]
    assert "{{WordFamily}}" in template["afmt"]


def test_qa_template():
    template = ModelTemplates.get_template(QAQuiz)

    # Test front template
    assert "{{Question}}" in template["qfmt"]
    assert "{{Source}}" in template["qfmt"]

    # Test back template
    assert "{{Answer}}" in template["afmt"]
    assert "{{Quotes}}" in template["afmt"]
    assert "{{KeyTerms}}" in template["afmt"]
    assert "{{RelatedConcepts}}" in template["afmt"]


def test_css_contains_required_styles():
    css = ModelTemplates.get_css()

    required_styles = [
        ".card",
        ".question",
        ".source",
        ".type-prompt",
        ".answer-section",
        ".meaning",
        ".examples",
        ".synonyms",
        ".antonyms",
        ".word-family",
        ".quotes",
        ".key-terms",
        ".related",
        "@media (max-width: 640px)",  # New mobile responsive style
    ]

    for style in required_styles:
        assert style in css


def test_css_contains_modern_design_elements():
    css = ModelTemplates.get_css()

    modern_elements = [
        "font-family: 'Inter'",
        "linear-gradient",
        "border-radius",
        "box-shadow",
        "background-color: #F7FAFC",
        "font-weight: 600",
    ]

    for element in modern_elements:
        assert element in css
