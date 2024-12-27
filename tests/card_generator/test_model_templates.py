import pytest
from anki_vocab_builder.card_generator.model_templates import ModelTemplates
from anki_vocab_builder.storage.models import TypeInQuiz, RecordingQuiz

@pytest.fixture
def sample_type_in_quiz():
    return TypeInQuiz(
        question="From Book: The Martian\nI guess I should explain how Mars missions work, for any _____ who may be reading this.",
        answer="layman",
        source="The Martian (Weir, Andy)",
        meaning="A person without professional knowledge in a particular subject",
        examples=["He explained the complex procedure in layman's terms."]
    )

@pytest.fixture
def sample_recording_quiz():
    return RecordingQuiz(
        question="What is the oldest and most fearsome god of all?",
        answer="the absent god",
        source="The Gervais Principle (Rao, Venkatesh)",
        context="Losing this illusion is a total-perspective-vortex moment for the Sociopath"
    )

def test_type_in_template():
    template = ModelTemplates.get_template(TypeInQuiz)
    
    assert "{{type:Answer}}" in template["qfmt"]
    assert "{{Source}}" in template["qfmt"]
    assert "{{Meaning}}" in template["afmt"]
    assert "{{Examples}}" in template["afmt"]

def test_recording_template():
    template = ModelTemplates.get_template(RecordingQuiz)
    
    assert "record-prompt" in template["qfmt"]
    assert "{{Question}}" in template["qfmt"]
    assert "{{Answer}}" in template["afmt"]
    assert "{{Context}}" in template["afmt"]

def test_css_contains_required_styles():
    css = ModelTemplates.get_css()
    
    required_styles = [
        ".source",
        ".question",
        ".type-prompt",
        ".record-prompt",
        ".answer",
        ".meaning"
    ]
    
    for style in required_styles:
        assert style in css 