from mistralai import Mistral
import os

api_key = os.getenv("MISTRAL_API_KEY")

model = "mistral-large-latest"

client = Mistral(api_key=api_key)

def stage_classifier(question: str) -> str:
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

                                    1. Introduction (Rapport building, asking general questions not related to the event and establishing the interview process.)
                                    2. Investigative (Asking questions about the event that took place)
                                    3. Closing (Exiting the interview.)

                                    Respond with only the stage.

                                    Classify {question}"""
                }
            ]
        )

        return chat_response.choices[0].message.content

    except Exception as e:
        print(f"Error calling Mistral API: {e}")
        return "MistralAI API call error."