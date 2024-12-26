from typing import List, Tuple
from openai import OpenAI
from pathlib import Path
from ..storage.models import VocabCard
from ..config import Config

class OpenAIEnricher:
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)


    def enrich_word(self, word: str) -> VocabCard:
        # Generate quiz question
        quiz_prompt = f"Create a fill-in-the-blank question for the word '{word}' that tests understanding of its meaning."
        quiz_response = self.client.chat.completions.create(
            model=self.config.GPT_MODEL,
            messages=[{"role": "user", "content": quiz_prompt}]
        )
        print(f"quiz repnse is {quiz_response}")
        quiz_question = quiz_response.choices[0].message.content

        # Generate meaning and examples
        content_prompt = f"Provide the following for the word '{word}':\n1. Brief meaning\n2. Three example sentences\n3. Pronunciation guide"
        content_response = self.client.chat.completions.create(
            model=self.config.GPT_MODEL,
            messages=[{"role": "user", "content": content_prompt}]
        )
        
        # Parse response (simplified for MVP)
        content = content_response.choices[0].message.content
        meaning, examples, pronunciation = self._parse_content(content)

        # Generate image
        image_response = self.client.images.generate(
            prompt=f"A simple illustration representing the word: {word}",
            size=self.config.DALLE_SIZE,
            model="dall-e-3",
            quality="standard",
            n=1
        )
        image_url = image_response.data[0].url
        
        # Save image (implementation needed)
        image_path = self._save_image(image_url, word)

        return VocabCard(
            word=word,
            quiz_question=quiz_question,
            meaning=meaning,
            example_sentences=examples,
            pronunciation=pronunciation,
            image_path=image_path
        )

    def _parse_content(self, content: str) -> Tuple[str, List[str], str]:
        # Simple parsing implementation - would need more robust parsing in production
        lines = content.split('\n')
        meaning = lines[0]
        examples = [line for line in lines if line.startswith('-')]
        pronunciation = lines[-1]
        return meaning, examples, pronunciation

    def _save_image(self, image_url: str, word: str) -> Path:
        # Implementation needed to download and save image
        pass