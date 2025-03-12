from mistralai import Mistral
import os

api_key = os.getenv("MISTRAL_API_KEY")

model = "mistral-large-latest"

client = Mistral(api_key=api_key)

def LLM_get_question_type(question: str) -> str:
    """
    Makes Mistral AI API call to classify a given question. This will be used as a backup when
    our finetuned classifier is unsure.

    Args:
        question: question to be classified

    Returns:
        str: category question has been classified as.
    """
    try:
        chat_response = client.chat.complete(
            model= model,
            messages = [
                {
                    "role": "user",
                    "content": f"""Categorise the question "{question}" into one of the categories.
                                Open-ended (A question that encourages an open answer and cannot be answered by yes or no. Sometimes starts with who, what, when, where, or how such as in 'What happened?')
                                Directive (A 'Who, What, When, Where, or How' question on a specific topic the question should suggest a short specific answer. )
                                Option-Posing (A multiple choice question (this also includes yes/no questions) where the answer is part of the question but is not implied your question should not suggest anything.)
                                Suggestive (Questions with presuppositions, implied correct answers, information that the interviewee did not reveal themselves.)
                                None of the above (statement or question that does not fit into the categories)."""
                }
            ]
        )

        return chat_response.choices[0].message.content

    except Exception as e:
        print(f"Error calling Mistral API: {e}")
        return "MistralAI API call error."



def LLM_get_stage(question: str) -> str:
    """
    Makes Mistral AI API call to classify a question into an interview stage.

    Args:
        question: question to be classified

    Returns:
        str: stage question has been classified as.
    """
    try:
        chat_response = client.chat.complete(
            model= model,
            messages = [
                {
                    "role": "user",
                    "content": f"""You receive questions from a police interview and classify them into one of the following stages:

                                    
Introduction (Rapport building, asking general questions not related to the event and establishing the interview process.)
Investigative (Asking questions about the event that took place)
Closing (Exiting the interview. Rapport building about the future, end-of-interview processes))

                                    Respond with only the stage.

                                    Classify {question}"""
                }
            ]
        )

        return chat_response.choices[0].message.content

    except Exception as e:
        #print(f"Error calling Mistral API: {e}")
        print("Error calling Mistral API")
        print(e)
        return "Introduction"
