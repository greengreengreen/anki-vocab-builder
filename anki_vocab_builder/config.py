import json
import os
from pathlib import Path
from typing import Dict


class Config:
    def __init__(self, config_path: Path = None, cache_dir: Path = None):
        self.config_path = config_path or Path.home() / ".anki_vocab_builder" / "config.json"
        self.config_dir = self.config_path.parent
        self.cache_dir = cache_dir or self.config_dir / "cache"

        # Create directories if they don't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Load or create config
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                return json.load(f)

        # Default config
        default_config = {
            "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
            "anki_deck_name": "Vocabulary",
            "anki_model_name": "Basic",
            "input_file": "words.csv",
            "force_refresh": False,
            "cache_max_age_days": 30,
            "cache_enabled": True,
            "output_dir": str(self.cache_dir),
            "image_generation": True,
            "audio_generation": True,
        }

        self.save_config(default_config)
        return default_config

    def save_config(self, config: Dict) -> None:
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4)
        self.config = config

    @property
    def openai_api_key(self) -> str:
        return self.config.get("openai_api_key", "")
