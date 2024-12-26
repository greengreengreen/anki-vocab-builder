from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    OPENAI_API_KEY: str
    INPUT_CSV_PATH: Path
    OUTPUT_ANKI_PATH: Path
    AUDIO_OUTPUT_DIR: Path = Path("audio_files")
    
    # OpenAI API settings
    GPT_MODEL: str = "gpt-4o-mini"
    DALLE_SIZE: str = "1024x1024"
