import json
from pathlib import Path
from typing import Dict


class Config:
    def __init__(self, config_path: Path = None):
        self.config_path = config_path or Path.home() / ".anki_vocab_builder" / "config.json"
        self.config_dir = self.config_path.parent

        # Create directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Load or create config
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                return json.load(f)

        # Default config
        default_config = {
            "anki_deck_name": "My kindle highlights",
            "anki_model_name": "Basic",
            "input_path": ".anki_vocab_builder/input/kindle/My Clippings.txt",
            "output_path": ".anki_vocab_builder/output/kindle_highlights.apkg",
            "batch_size": 10,
            "force_refresh": False,
            "cache_max_age_days": 30,
            "gpt_model": "gpt-4o"
        }

        self.save_config(default_config)
        return default_config

    def save_config(self, config: Dict) -> None:
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4)
        self.config = config

    @property
    def anki_deck_name(self) -> str:
        return self.config.get("anki_deck_name", "My kindle highlights")

    @property
    def anki_model_name(self) -> str:
        return self.config.get("anki_model_name", "Basic")

    @property
    def input_path(self) -> Path:
        return Path(self.config.get("input_path", ".anki_vocab_builder/input/kindle/My Clippings.txt"))

    @property
    def output_path(self) -> Path:
        return Path(self.config.get("output_path", ".anki_vocab_builder/output/kindle_highlights.apkg"))

    @property
    def batch_size(self) -> int:
        return self.config.get("batch_size", 10)

    @property
    def force_refresh(self) -> bool:
        return self.config.get("force_refresh", False)

    @property
    def cache_max_age_days(self) -> int:
        return self.config.get("cache_max_age_days", 30)

    @property
    def gpt_model(self) -> str:
        return self.config.get("gpt_model", "gpt-4o")
