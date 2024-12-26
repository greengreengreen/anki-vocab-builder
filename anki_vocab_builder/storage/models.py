from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class VocabCard:
    word: str
    quiz_question: str
    meaning: str
    example_sentences: List[str]
    pronunciation: str
    image_path: Optional[Path] = None
    audio_path: Optional[Path] = None
