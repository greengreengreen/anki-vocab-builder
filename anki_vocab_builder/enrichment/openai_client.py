import hashlib
import json
import os
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from openai import OpenAI

from ..config import Config
from ..storage.models import VocabCard


class OpenAIClient:
    def __init__(self, config: Config):
        self.config = config
        self.cache_dir = config.cache_dir
        self.client = OpenAI(api_key=config.openai_api_key)

        # Create cache file if it doesn't exist
        self.cache_file = self.cache_dir / "openai_cache.json"
        if not self.cache_file.exists():
            self.cache_file.write_text("{}")

        # Load cache
        self.cache = self._load_cache()

    def _load_cache(self):
        """Load cache from file or create new cache"""
        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_cache(self):
        """Save cache to file"""
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)

    def _get_cache_key(self, prompt: str, type: str) -> str:
        """Generate a unique cache key for a prompt"""
        return hashlib.md5(f"{type}:{prompt}".encode()).hexdigest()

    def _should_use_cache(self, force_refresh: bool = None) -> bool:
        """Determine if cache should be used based on config and override"""
        if force_refresh is not None:
            return not force_refresh
        return self.config.config.get("cache_enabled", True) and not self.config.config.get(
            "force_refresh", False
        )

    def _get_cached_response(
        self, prompt: str, type: str, force_refresh: bool = None
    ) -> Optional[str]:
        """Get cached response if it exists and isn't too old"""
        if not self._should_use_cache(force_refresh):
            return None

        cache_key = self._get_cache_key(prompt, type)
        cached_data = self.cache.get(cache_key, {})

        if cached_data:
            max_age_days = self.config.config.get("cache_max_age_days", 30)
            age = time.time() - cached_data.get("timestamp", 0)
            if age < max_age_days * 24 * 3600:  # Convert days to seconds
                return cached_data.get("response")
        return None

    def _cache_response(self, prompt: str, type: str, response: str):
        """Cache a response"""
        cache_key = self._get_cache_key(prompt, type)
        self.cache[cache_key] = {"response": response, "timestamp": time.time()}
        self._save_cache()

    def enrich_word(self, word: str, force_refresh: bool = None) -> Dict:
        """Enrich a word with quiz, content, and image."""
        try:
            # Get quiz question
            quiz_prompt = f"Create a fill-in-the-blank question for the word '{word}' that tests understanding of its meaning."
            quiz_question = self._get_cached_response(quiz_prompt, "quiz", force_refresh=force_refresh)

            if not quiz_question:
                quiz_response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": quiz_prompt}]
                )
                quiz_question = quiz_response.choices[0].message.content
                self._cache_response(quiz_prompt, "quiz", quiz_question)

            # Get content
            content_prompt = (
                f"Provide information about the word '{word}' in this format:\n"
                "1. Brief definition\n"
                "- Example sentence 1\n"
                "- Example sentence 2\n"
                "- Example sentence 3\n"
                "Pronunciation: /phonetic/"
            )
            content = self._get_cached_response(content_prompt, "content", force_refresh=force_refresh)

            if not content:
                content_response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": content_prompt}]
                )
                content = content_response.choices[0].message.content
                self._cache_response(content_prompt, "content", content)

            # Parse the content
            meaning, example_sentences, pronunciation = self._parse_content(content)

            # Generate image
            image_prompt = f"A simple illustration representing the word: {word}"
            image_url = self._get_cached_response(image_prompt, "image", force_refresh=force_refresh)

            if not image_url:
                image_response = self.client.images.generate(
                    prompt=image_prompt,
                    size="1024x1024",
                    model="dall-e-3",
                    quality="standard",
                    n=1
                )
                image_url = image_response.data[0].url
                self._cache_response(image_prompt, "image", image_url)

            # Save the image locally
            image_path = self._save_image(image_url, word)

            return {
                "word": word,
                "quiz_question": quiz_question,
                "meaning": meaning,
                "example_sentences": example_sentences,
                "pronunciation": pronunciation,
                "image_url": image_url,
                "image_path": str(image_path)
            }

        except Exception as e:
            print(f"Error enriching word '{word}': {str(e)}")
            raise

    def _parse_content(self, content: str) -> Tuple[str, List[str], str]:
        """Parse the content response from OpenAI into structured data."""
        try:
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            # Extract meaning (first line after "1." or first line)
            meaning = ""
            for line in lines:
                if line.startswith("1."):
                    meaning = line[2:].strip()
                    break
            if not meaning and lines:
                meaning = lines[0]

            # Extract example sentences (lines starting with "-" or numbered)
            example_sentences = []
            for line in lines:
                if line.startswith("-") or (line[0].isdigit() and line[1] in ".)"):
                    cleaned_line = line.lstrip("0123456789.) -").strip()
                    if cleaned_line:
                        example_sentences.append(cleaned_line)

            # Extract pronunciation (last line or line containing phonetic symbols)
            pronunciation = ""
            for line in reversed(lines):
                if "/" in line or any(char in line for char in "[]()"):
                    pronunciation = line.strip()
                    break
            if not pronunciation and lines:
                pronunciation = lines[-1]

            return meaning, example_sentences, pronunciation

        except Exception as e:
            # Fallback parsing if structured parsing fails
            return (
                "Definition not available",
                ["No examples available"],
                "Pronunciation not available"
            )

    def _save_image(self, image_url: str, word: str) -> Path:
        """Download and save an image from a URL.

        Args:
            image_url: The URL of the image to download
            word: The vocabulary word associated with the image

        Returns:
            Path: The path where the image was saved
        """
        # Create images directory if it doesn't exist
        images_dir = self.cache_dir / "images"
        images_dir.mkdir(exist_ok=True)

        # Generate a filename using the word and URL hash to ensure uniqueness
        url_hash = hashlib.md5(image_url.encode()).hexdigest()[:8]
        file_name = f"{word}_{url_hash}.png"
        file_path = images_dir / file_name

        # Download the image if it doesn't already exist
        if not file_path.exists():
            response = requests.get(image_url)
            response.raise_for_status()  # Raise an exception for bad status codes

            with open(file_path, "wb") as f:
                f.write(response.content)

        return file_path
