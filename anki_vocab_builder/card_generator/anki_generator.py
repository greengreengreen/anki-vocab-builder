import genanki
from typing import List
from pathlib import Path
from ..storage.models import VocabCard

class AnkiGenerator:
    def __init__(self, output_path: Path):
        self.output_path = output_path
        self.model = genanki.Model(
            1607392319,
            'Vocab Model',
            fields=[
                {'name': 'Word'},
                {'name': 'Quiz'},
                {'name': 'Meaning'},
                {'name': 'Examples'},
                {'name': 'Pronunciation'},
                {'name': 'Image'},
                {'name': 'Audio'}
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Quiz}}<br>{{Audio}}',
                    'afmt': '''
                        {{FrontSide}}
                        <hr id="answer">
                        <b>Word:</b> {{Word}}<br>
                        <b>Meaning:</b> {{Meaning}}<br>
                        <b>Examples:</b> {{Examples}}<br>
                        <b>Pronunciation:</b> {{Pronunciation}}<br>
                        {{#Image}}<img src="{{Image}}">{{/Image}}
                    ''',
                },
            ])

    def generate_deck(self, cards: List[VocabCard], deck_name: str = "Vocabulary") -> None:
        deck = genanki.Deck(2059400110, deck_name)

        for card in cards:
            note = genanki.Note(
                model=self.model,
                fields=[
                    card.word,
                    card.quiz_question,
                    card.meaning,
                    '<br>'.join(card.example_sentences),
                    card.pronunciation,
                    str(card.image_path) if card.image_path else '',
                    str(card.audio_path) if card.audio_path else ''
                ]
            )
            deck.add_note(note)

        package = genanki.Package(deck)
        package.write_to_file(self.output_path)
