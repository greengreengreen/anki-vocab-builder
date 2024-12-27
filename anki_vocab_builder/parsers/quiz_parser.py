from typing import List, Union
from ..storage.models import TypeInQuiz, QAQuiz

class QuizParser:
    @staticmethod
    def parse_quiz(gpt_response: dict) -> Union[TypeInQuiz, QAQuiz]:
        """Parse ChatGPT's response into appropriate quiz type"""
        quiz_type = gpt_response.get("type")
        
        if quiz_type == "type_in":
            return TypeInQuiz(
                question=gpt_response["question"],
                answer=gpt_response["answer"],
                source=gpt_response["source"],
                meaning=gpt_response.get("meaning"),
                examples=gpt_response.get("examples", [])
            )
        elif quiz_type == "qa":
            return QAQuiz(
                question=gpt_response["question"],
                answer=gpt_response["answer"],
                source=gpt_response["source"],
                quotes=gpt_response.get("quotes", [])
            )
        else:
            raise ValueError(f"Unknown quiz type: {quiz_type}")

    @staticmethod
    def parse_quiz_list(gpt_responses: List[dict]) -> List[Union[TypeInQuiz, QAQuiz]]:
        """Parse a list of ChatGPT responses into quizzes"""
        return [QuizParser.parse_quiz(response) for response in gpt_responses] 