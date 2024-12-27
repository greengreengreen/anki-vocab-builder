from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod
from pathlib import Path

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
    question: str    # The fill-in-blank question
    answer: str      # The word to be typed
    source: str      # Book/article title and author
    meaning: Optional[str] = None
    examples: Optional[List[str]] = None
    tags: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    
    def get_model_id(self) -> int:
        return 1607392319
    
    def get_model_name(self) -> str:
        return "Type-In Quiz"
    
    def get_fields(self) -> List[str]:
        return ["Question", "Answer", "Source", "Meaning", "Examples"]
    
    def get_field_values(self) -> List[str]:
        return [
            self.question,
            self.answer,
            self.source,
            self.meaning or "",
            "<br>".join(self.examples) if self.examples else ""
        ]

@dataclass
class QAQuiz(BaseQuiz):
    question: str
    answer: str
    source: str      # Book/article title and author
    quotes: Optional[List[str]] = None
    tags: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    
    def get_model_id(self) -> int:
        return 1607392320
    
    def get_model_name(self) -> str:
        return "Q&A Quiz"
    
    def get_fields(self) -> List[str]:
        return ["Question", "Answer", "Source", "Quotes"]
    
    def get_field_values(self) -> List[str]:
        return [
            self.question,
            self.answer,
            self.source,
            "<br><br>".join(self.quotes) if self.quotes else ""
        ]
