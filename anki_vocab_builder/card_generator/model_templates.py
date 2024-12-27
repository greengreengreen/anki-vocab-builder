from typing import Dict, Type

from ..storage.models import BaseQuiz, QAQuiz, TypeInQuiz


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
                """,
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
                """,
            },
        }
        return templates.get(quiz_type, {})

    @staticmethod
    def get_css() -> str:
        """Get common CSS for all templates"""
        return """
        /* Modern Card Design */
        .card {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            text-align: left;
            color: #2D3748;
            background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            max-width: 800px;
            margin: 0 auto;
        }

        /* Question Styling */
        .question {
            font-size: 1.25rem;
            font-weight: 600;
            color: #1A365D;
            margin-bottom: 1.5rem;
            padding: 1rem;
            background-color: #EBF8FF;
            border-radius: 8px;
            border-left: 4px solid #4299E1;
        }

        /* Source Citation */
        .source {
            color: #718096;
            font-style: italic;
            margin-bottom: 1.5rem;
            font-size: 0.9rem;
        }

        /* Type-in Prompt */
        .type-prompt {
            color: #4A5568;
            margin-bottom: 0.75rem;
            font-weight: 500;
        }

        /* Answer Section */
        .answer-section {
            margin: 1.5rem 0;
            padding: 1rem;
            background-color: #F7FAFC;
            border-radius: 8px;
        }

        .user-answer {
            margin-bottom: 0.75rem;
            color: #2C5282;
        }

        .correct-answer {
            color: #276749;
            font-weight: 500;
        }

        /* Content Sections */
        .meaning, .examples, .synonyms, .antonyms, .word-family,
        .quotes, .key-terms, .related {
            margin-top: 1.25rem;
            padding: 1rem;
            background-color: white;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }

        /* Section Headers */
        .meaning::before, .examples::before, .synonyms::before,
        .antonyms::before, .word-family::before, .quotes::before,
        .key-terms::before, .related::before {
            display: block;
            font-weight: 600;
            color: #4A5568;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Examples Section */
        .examples {
            background-color: #F0FFF4;
            border-color: #9AE6B4;
        }

        /* Synonyms & Antonyms */
        .synonyms, .antonyms {
            display: inline-block;
            margin-right: 1rem;
            background-color: #F7FAFC;
        }

        /* Word Family Section */
        .word-family {
            background-color: #EDF2F7;
            font-family: 'Fira Code', monospace;
        }

        /* Quotes Section */
        .quotes {
            background-color: #FEFCBF;
            border-left: 4px solid #ECC94B;
            font-style: italic;
        }

        /* Divider */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(to right, #E2E8F0, #CBD5E0, #E2E8F0);
            margin: 1.5rem 0;
        }

        /* Mobile Responsiveness */
        @media (max-width: 640px) {
            .card {
                padding: 1rem;
                font-size: 15px;
            }

            .question {
                font-size: 1.1rem;
            }
        }
        """
