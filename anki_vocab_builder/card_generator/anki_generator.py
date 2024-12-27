from pathlib import Path
from typing import Dict, List, Type

import genanki

from ..storage.models import BaseQuiz
from .model_templates import ModelTemplates


class AnkiGenerator:
    def __init__(self, output_path: Path):
        self.output_path = output_path
        self.models: Dict[Type[BaseQuiz], genanki.Model] = {}

    def _get_or_create_model(self, quiz: BaseQuiz) -> genanki.Model:
        """Get existing model or create new one for quiz type"""
        quiz_type = type(quiz)

        if quiz_type not in self.models:
            template = ModelTemplates.get_template(quiz_type)

            self.models[quiz_type] = genanki.Model(
                quiz.get_model_id(),
                quiz.get_model_name(),
                fields=[{"name": field} for field in quiz.get_fields()],
                templates=[template],
                css=ModelTemplates.get_css(),
            )

        return self.models[quiz_type]

    def generate_deck(self, quizzes: List[BaseQuiz], deck_name: str = "Quiz Deck") -> None:
        deck = genanki.Deck(2059400110, deck_name)

        for quiz in quizzes:
            model = self._get_or_create_model(quiz)

            note = genanki.Note(model=model, fields=quiz.get_field_values(), tags=quiz.tags)
            deck.add_note(note)

        package = genanki.Package(deck)
        package.write_to_file(self.output_path)
