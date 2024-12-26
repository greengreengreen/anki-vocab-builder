from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path

@dataclass
class VocabCard:
    word: str
    quiz_question: str
    meaning: str
    example_sentences: List[str]
    pronunciation: str
    image_path: Optional[Path] = None
    audio_path: Optional[Path] = None
