import os
from mistralai import Mistral
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

model = "mistral-large-latest"

client = Mistral(api_key=api_key)

prompt_content = """Your task is to generate scenarios for an investigative interviewer to imagine themselves within. The interviewer primarily works with abused children (including sexual), up to age 18. Please generate a scenario of the form: Scenario: [Scenario] Age: [age]. The scenario should be short, include no dialogue and only have a few details. The setting is a court, so the scenario should just be some brief information about evidence. Also include the name and age of the child as separate fields. They cannot be named Lucas.

Here is an example: 

Scenario: A six-year-old girl named Emily is brought to testify in court regarding allegations of physical abuse. The interviewer is provided with photographs and drawings made by Emily, depicting unexplained bruises and injuries on her body. There are also medical reports detailing multiple fractures, some healing and others still active. A worn teddy bear, belonging to Emily, has been collected as evidence from the home and shows signs of being used as a weapon. The courtroom is filled with tension as Emily bravely faces her accused abuser in the witness box

Name: Emily
Age: 6 """

def parse_text_to_dict(text):
    lines = text.strip().split("\n")
    data = {}

    for line in lines:
        if ": " in line:
            key, value = line.split(": ", 1)  
            data[key.strip()] = value.strip()

    return data

def create_scenario():
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



