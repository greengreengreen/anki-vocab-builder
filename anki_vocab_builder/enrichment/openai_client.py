from pathlib import Path
from typing import List, Dict, Any
import json
import os
from openai import OpenAI
import tqdm

from anki_vocab_builder.parsers.kindle_highlights import parse_kindle_clippings
from anki_vocab_builder.enrichment.openai_prompts import BATCH_SYSTEM_PROMPT, BATCH_USER_PROMPT


class OpenAIClient:
    def __init__(self, api_key: str, batch_size: int = 10, cache_dir: Path = None):
        """Initialize OpenAI client with API key and optional cache directory."""
        self.client = OpenAI(api_key=api_key)
        self.cache_dir = cache_dir or Path(".cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "openai_cache.json"
        self.cache = self._load_cache()
        self.batch_size = batch_size

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
        all_quizzes = []
        
        for i in tqdm.tqdm(range(0, len(highlights), self.batch_size)):
            batch = highlights[i:i + self.batch_size]
            cache_key = self._get_cache_key(batch)
            
            # Check cache first
            if cache_key in self.cache:
                all_quizzes.extend(self.cache[cache_key])
                continue
                
            formatted_highlights = " \n\n ".join(
                f"Highlight {j+1}: \n {highlight} \n Source: {source}"
                for j, (highlight, source, _) in enumerate(batch)
            )
            
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": BATCH_SYSTEM_PROMPT},
                        {"role": "user", "content": BATCH_USER_PROMPT.format(highlights=formatted_highlights)}
                    ],
                    response_format={"type": "text"}
                )
                content = response.choices[0].message.content

                start_index = content.find("[")
                end_index = content.rfind("]") + 1
                json_str = content[start_index:end_index]
                result = json.loads(json_str)
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
    

if __name__ == "__main__":
    client = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"))
    res = client.process_kindle_highlights(Path(".anki_vocab_builder/input/kindle/My Clippings.txt"))
    print(res)
