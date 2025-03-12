import os
from mistralai import Mistral
import os
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

model = "mistral-large-latest"

client = Mistral(api_key=api_key)

prompt_content = """Your task is to generate scenarios for an investigative interviewer to imagine themselves within. The interviewer primarily works with abused children (including sexual), up to age 18. Please generate a scenario of the form: Scenario: [Scenario] Age: [age]. The scenario should be short, include no dialogue and only have a few details. The scenario should just be some brief information about evidence. Also include the name and age of the child as separate fields. They cannot be named Lucas.

Here is an example: 

Scenario: A six-year-old girl named Emily is brought to testify in court regarding allegations of physical abuse. The interviewer is provided with photographs and drawings made by Emily, depicting unexplained bruises and injuries on her body. There are also medical reports detailing multiple fractures, some healing and others still active. A worn teddy bear, belonging to Emily, has been collected as evidence from the home and shows signs of being used as a weapon.

Name: Emily
Age: 6 """

def parse_text_to_dict(text) -> Dict[str, str]:
    """
    Helper function to parse text into a dictionary. This is used to extract Scenario, Name, and Age from the generated text.

    Args:
        text (str): The text to parse.

    Returns:
        dict: A dictionary containing the parsed key-value
    """

    lines = text.strip().split("\n")
    data = {}

    for line in lines:
        if ": " in line:
            key, value = line.split(": ", 1)  
            data[key.strip()] = value.strip()

    return data

def create_scenario() -> Dict[str, str]:
    """
    Generates a scenario using the Mistral API.

    Returns:
        dict: A dictionary containing the generated scenario.
    """

    try:
        chat_response = client.chat.complete(
            model= model,
            messages = [
                {
                    "role": "user",
                    "content": prompt_content,
                },
            ]
        )
            
        text = chat_response.choices[0].message.content
        return parse_text_to_dict(text)
    except Exception as e:
        print(f"Error calling mistral api: {e}")
        return "This is an error message, something went wrong :("



