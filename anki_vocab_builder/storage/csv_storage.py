import csv
from pathlib import Path
from typing import List

from .models import VocabCard


class CSVStorage:
    def __init__(self, input_path: Path):
        self.input_path = input_path

    def read_words(self) -> List[str]:
        with open(self.input_path, "r") as f:
            reader = csv.reader(f)
            return [row[0].strip() for row in reader]
