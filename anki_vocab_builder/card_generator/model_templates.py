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
                """
            }
        }
        return templates.get(quiz_type, {})

    @staticmethod
    def get_css() -> str:
        """Get common CSS for all templates"""
        return """
            /* Card container */
            .card {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                max-width: 800px;
                margin: 30px auto;
                padding: 30px;
                background: linear-gradient(to bottom right, #ffffff, #f8f9fa);
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
                transition: transform 0.2s ease;
            }

            .card:hover {
                transform: translateY(-2px);
            }

            /* Question styling */
            .question {
                font-size: 1.8em;
                color: #2c3e50;
                margin-bottom: 25px;
                line-height: 1.5;
                font-weight: 600;
                text-align: center;
                padding: 20px;
                border-radius: 12px;
                background: rgba(255, 255, 255, 0.8);
                box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
            }

            /* Source styling */
            .source {
                font-style: italic;
                color: #7f8c8d;
                margin: 20px 0;
                font-size: 1.1em;
                border-left: 4px solid #3498db;
                padding: 10px 20px;
                background: rgba(52, 152, 219, 0.05);
                border-radius: 0 8px 8px 0;
            }

            /* Type prompt styling */
            .type-prompt {
                color: #34495e;
                margin: 20px 0;
                font-size: 1.3em;
                text-align: center;
                font-weight: 500;
            }

            /* Answer styling */
            .answer {
                font-weight: 600;
                margin: 25px 0;
                color: #2980b9;
                font-size: 1.6em;
                text-align: center;
                padding: 20px;
                background: rgba(41, 128, 185, 0.1);
                border-radius: 12px;
                border: 2px solid rgba(41, 128, 185, 0.2);
            }

            /* Meaning section */
            .meaning {
                margin: 25px 0;
                color: #27ae60;
                line-height: 1.6;
                padding: 20px;
                background: rgba(39, 174, 96, 0.1);
                border-radius: 12px;
                font-size: 1.2em;
            }

            /* Examples and Quotes sections */
            .examples, .quotes {
                margin: 25px 0;
                color: #555;
                line-height: 1.7;
                background: #f8f9fa;
                padding: 20px;
                border-radius: 12px;
                box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.05);
            }

            /* Horizontal rule styling */
            hr {
                border: none;
                height: 2px;
                background: linear-gradient(to right, transparent, #e0e0e0, transparent);
                margin: 30px 0;
            }

            /* Input field styling for type-in cards */
            input {
                font-size: 1.3em;
                padding: 12px 16px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                width: 100%;
                margin: 15px 0;
                transition: all 0.3s ease;
                background: rgba(255, 255, 255, 0.9);
            }

            input:focus {
                border-color: #3498db;
                outline: none;
                box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
                transform: translateY(-1px);
            }

            /* Night mode adjustments */
            .nightMode .card {
                background: linear-gradient(to bottom right, #2c3e50, #2c3e50);
                color: #ecf0f1;
            }

            .nightMode .question {
                background: rgba(255, 255, 255, 0.05);
                color: #ecf0f1;
            }

            .nightMode input {
                background: rgba(255, 255, 255, 0.1);
                color: #ecf0f1;
                border-color: #34495e;
            }

            .nightMode .source {
                border-left-color: #3498db;
                background: rgba(52, 152, 219, 0.1);
            }

            .nightMode .answer {
                background: rgba(41, 128, 185, 0.2);
                color: #3498db;
            }

            .nightMode .meaning {
                background: rgba(39, 174, 96, 0.1);
            }

            .nightMode .examples, .nightMode .quotes {
                background: rgba(255, 255, 255, 0.05);
                color: #bdc3c7;
            }
        """ 