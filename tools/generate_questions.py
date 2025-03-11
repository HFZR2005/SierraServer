from mistralai import Mistral
import random
import os

api_key = os.getenv("MISTRAL_API_KEY")

model = "mistral-large-latest"

client = Mistral(api_key=api_key)

def get_question_category() -> str:
    """
    Randomly assigns one of the question categories for the LLM to generate.

    Returns:
        str: category to be generated, includes a description of the type of question for the LLM
    """

    return random.choice([
        "Open-ended (A question that encourages a open answer and cannot be answered by yes or no, they do not start with what, where, when, how, or, why) ", 
        "Directive (A 'Who, What, When, Where, or How' question on a specific topic the question should suggest a short specific answer. )", 
        "Option-Posing (A multiple choice question (this also includes yes/no questions) where the answer is part of the question but is not implied your question should not suggest anything.)", 
        "Suggestive (Questions with presuppositions, implied correct answers, information that the interviewee did not reveal themselves.)"
    ])

def LLM_generate_question(category: str) -> str:
    """
    Makes Mistral AI API call to generate a "category" question.

    Args:
        category: the category the generated question should be of. Includes a description aswell

    Returns:
        str: generated question

    """
    try:
        chat_response = client.chat.complete(
            model = model,
            messages = [
                {
                    "role": "user",
                    "content":
                    "You are the police interviewing a child about their abuse. Give only questions. Give me a " + category + " question. "
                }
            ]
        )

        return chat_response.choices[0].message.content

    except Exception as e:
        print(f"Error calling Mistral API: {e}")
        return "MistralAI API call error."


