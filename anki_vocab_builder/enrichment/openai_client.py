from pathlib import Path
from typing import List, Dict, Any
import json
import os
from openai import OpenAI

from ..parsers.kindle_highlights import parse_kindle_clippings
from .openai_prompts import BATCH_SYSTEM_PROMPT, BATCH_USER_PROMPT


class OpenAIClient:
    def __init__(self, api_key: str, cache_dir: Path = None):
        """Initialize OpenAI client with API key and optional cache directory."""
        self.client = OpenAI(api_key=api_key)
        self.cache_dir = cache_dir or Path(".cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "openai_cache.json"
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict:
        """Load cache from file or create new cache."""
        if self.cache_file.exists():
            return json.loads(self.cache_file.read_text())
        return {}

    def _save_cache(self):
        """Save cache to file."""
        self.cache_file.write_text(json.dumps(self.cache, indent=2))

    def _get_cache_key(self, highlights: List[tuple]) -> str:
        """Generate cache key from highlights."""
        content = json.dumps(highlights, sort_keys=True)
        return f"batch_{hash(content)}"

    def process_kindle_highlights(self, clippings_path: Path) -> List[Dict[str, Any]]:
        """Process Kindle highlights and generate quizzes with caching."""
        highlights = parse_kindle_clippings(clippings_path)
        batch_size = 5
        all_quizzes = []
        
        for i in range(0, len(highlights), batch_size):
            batch = highlights[i:i + batch_size]
            cache_key = self._get_cache_key(batch)
            
            # Check cache first
            if cache_key in self.cache:
                all_quizzes.extend(self.cache[cache_key])
                continue
                
            formatted_highlights = "\n\n".join(
                f"Highlight {j+1}:\n{highlight}\nSource: {source}"
                for j, (highlight, source) in enumerate(batch)
            )
            
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": BATCH_SYSTEM_PROMPT},
                        {"role": "user", "content": BATCH_USER_PROMPT.format(highlights=formatted_highlights)}
                    ],
                    response_format={"type": "json_object"}
                )
                
                result = json.loads(response.choices[0].message.content)
                if isinstance(result, list):
                    self.cache[cache_key] = result
                    all_quizzes.extend(result)
                else:
                    self.cache[cache_key] = [result]
                    all_quizzes.append(result)
                
                # Save cache after each successful batch
                self._save_cache()
                    
            except Exception as e:
                print(f"Error processing batch {i//batch_size + 1}: {str(e)}")
                continue
                
        return all_quizzes
