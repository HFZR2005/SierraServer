from mistralai import Mistral
import random
import os

api_key = os.getenv("MISTRAL_API_KEY")

model = "mistral-large-latest"

client = Mistral(api_key=api_key)

def get_question_category():
    return random.choice([
    "Open-ended (A question that encourages a open answer and cannot be answered by yes or no.)", 
    "Directive (A 'Who, What, When, Where, or How' question on a specific topic. )", 
    "Option Posing (A multiple choice question (this also includes yes/no questions) where the answer is part of the question but is not implied.)", 
    "Suggestive (Questions with presuppositions, implied correct answers, information that the interviewee did not reveal themselves.)"
    ])

def generate_category_question(category):
    try:
        chat_response = client.chat.complete(
            model= model,
            messages = [
                {
                    "role": "system",
                    "content": 
                    "You are the police interviewing a child about their abuse. Give only questions.",

                    "role": "user",
                    "content":
                    "Give me a " + category + " question. "
                },
            ]
        )

        return chat_response.choices[0].message.content

    except Exception as e:
        print(f"Error calling Mistral API: {e}")
        return "LLM API call error."


