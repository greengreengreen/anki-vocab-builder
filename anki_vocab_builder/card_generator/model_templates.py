from typing import Dict, Type
from ..storage.models import BaseQuiz, TypeInQuiz, QAQuiz

class ModelTemplates:
    """Collection of Anki model templates"""
    
    @staticmethod
    def get_template(quiz_type: Type[BaseQuiz]) -> Dict:
        """Get the appropriate template for a quiz type"""
        templates = {
            TypeInQuiz: {
                "name": "Type-In Card",
                "qfmt": """
                    <div class="question">{{Question}}</div>
                    <div class="source">Source: {{Source}}</div>
                    <div class="type-prompt">Type your answer:</div>
                    {{type:Answer}}
                """,
                "afmt": """
                    <div class="question">{{Question}}</div>
                    <div class="source">Source: {{Source}}</div>
                    <hr>
                    <div class="answer-section">
                        <div class="user-answer">Your answer: {{type:Answer}}</div>
                        <div class="correct-answer">Correct answer: {{Answer}}</div>
                    </div>
                    {{#Meaning}}
                    <div class="meaning">Meaning: {{Meaning}}</div>
                    {{/Meaning}}
                    {{#Examples}}
                    <div class="examples">Examples:<br>{{Examples}}</div>
                    {{/Examples}}
                    {{#Synonyms}}
                    <div class="synonyms">Synonyms: {{Synonyms}}</div>
                    {{/Synonyms}}
                    {{#Antonyms}}
                    <div class="antonyms">Antonyms: {{Antonyms}}</div>
                    {{/Antonyms}}
                    {{#WordFamily}}
                    <div class="word-family">Word Family:<br>{{WordFamily}}</div>
                    {{/WordFamily}}
                """
            },
            QAQuiz: {
                "name": "Q&A Card",
                "qfmt": """
                    <div class="question">{{Question}}</div>
                    <div class="source">Source: {{Source}}</div>
                """,
                "afmt": """
                    <div class="question">{{Question}}</div>
                    <div class="source">Source: {{Source}}</div>
                    <hr>
                    <div class="answer">{{Answer}}</div>
                    {{#Quotes}}
                    <div class="quotes">Quotes from the book:<br>{{Quotes}}</div>
                    {{/Quotes}}
                    {{#KeyTerms}}
                    <div class="key-terms">Key Terms:<br>{{KeyTerms}}</div>
                    {{/KeyTerms}}
                    {{#RelatedConcepts}}
                    <div class="related">Related Concepts:<br>{{RelatedConcepts}}</div>
                    {{/RelatedConcepts}}
                """
            }
        }
        return templates.get(quiz_type, {})

    @staticmethod
    def get_css() -> str:
        """Get common CSS for all templates"""
        return """
        .card {
            font-family: Arial, sans-serif;
            font-size: 16px;
            text-align: left;
            color: black;
            background-color: white;
            padding: 20px;
        }
        
        .question {
            font-size: 18px;
            margin-bottom: 15px;
        }
        
        .source {
            color: #666;
            font-style: italic;
            margin-bottom: 15px;
        }
        
        .type-prompt {
            color: #444;
            margin-bottom: 5px;
        }
        
        .answer-section {
            margin: 15px 0;
        }
        
        .meaning, .examples, .synonyms, .antonyms, .word-family,
        .quotes, .key-terms, .related {
            margin-top: 15px;
            padding: 10px;
            background-color: #f5f5f5;
            border-radius: 5px;
        }
        
        hr {
            border: none;
            border-top: 1px solid #ddd;
            margin: 20px 0;
        }
    """