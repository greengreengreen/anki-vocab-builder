from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class BaseQuiz(ABC):
    """Abstract base class for all quiz types"""

    @abstractmethod
    def get_model_name(self) -> str:
        """Return model name for this quiz type"""
        pass

    @abstractmethod
    def get_fields(self) -> List[str]:
        """Return list of field names for this quiz type"""
        pass

    @abstractmethod
    def get_field_values(self) -> List[str]:
        """Return list of field values for this quiz type"""
        pass


@dataclass
class TypeInQuiz(BaseQuiz):
    question: str  # The fill-in-blank question
    answer: str  # The word to be typed
    source: str  # Book/article title and author
    meaning: Optional[str] = None
    examples: Optional[List[str]] = None
    synonyms: Optional[List[str]] = None
    antonyms: Optional[List[str]] = None
    word_family: Optional[Dict[str, List[str]]] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)

    def get_model_id(self) -> int:
        return 1607392319

    def get_model_name(self) -> str:
        return "Type-In Quiz"

    def get_fields(self) -> List[str]:
        return [
            "Question",
            "Answer",
            "Source",
            "Meaning",
            "Examples",
            "Synonyms",
            "Antonyms",
            "WordFamily",
        ]

    def get_field_values(self) -> List[str]:
        word_family_str = ""
        if self.word_family:
            parts = []
            for pos, words in self.word_family.items():
                if words:
                    parts.append(f"{pos.title()}: {', '.join(words)}")
            word_family_str = "<br>".join(parts)

        return [
            self.question,
            self.answer,
            self.source,
            self.meaning or "",
            "<br>".join(self.examples) if self.examples else "",
            ", ".join(self.synonyms) if self.synonyms else "",
            ", ".join(self.antonyms) if self.antonyms else "",
            word_family_str,
        ]


@dataclass
class QAQuiz(BaseQuiz):
    question: str
    answer: str
    source: str
    quotes: Optional[List[str]] = None
    key_terms: Optional[List[Dict[str, str]]] = None
    related_concepts: Optional[List[str]] = None
    tags: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)

    def get_model_id(self) -> int:
        return 1607392320

    def get_model_name(self) -> str:
        return "Q&A Quiz"

    def get_fields(self) -> List[str]:
        return ["Question", "Answer", "Source", "Quotes", "KeyTerms", "RelatedConcepts"]

    def get_field_values(self) -> List[str]:
        key_terms_str = ""
        if self.key_terms:
            terms = []
            for term in self.key_terms:
                parts = []
                if "term" in term:
                    parts.append(f"<b>{term['term']}</b>")
                if "definition" in term:
                    parts.append(f"Definition: {term['definition']}")
                if "usage" in term:
                    parts.append(f"Usage: {term['usage']}")
                terms.append(" - ".join(parts))
            key_terms_str = "<br><br>".join(terms)

        return [
            self.question,
            self.answer,
            self.source,
            "<br><br>".join(self.quotes) if self.quotes else "",
            key_terms_str,
            "<br>".join(self.related_concepts) if self.related_concepts else "",
        ]
