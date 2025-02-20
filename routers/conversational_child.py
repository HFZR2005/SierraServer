import os
from mistralai import Mistral
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate 

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

model = "mistral-large-latest"

client = Mistral(api_key=api_key)

# create a prompt template with holes for the conversation history and the user's input 

prompt_template = PromptTemplate.from_template(
    """ 
    You are a child talking to an interviewer. You are being questioned for evidence of a crime that has happened against you. The scenario is:

    {scenario}

    You are to play the role of the child in this scenario. Please ensure that your responses are consistent with the scenario.

    The conversation so far has been: 

    {history}

    The interviewer says:

    {prompt_content}

    You respond:

    """
)


def get_child_response(scenario, history, prompt_content):
    message_content = prompt_template.invoke({
        "scenario":scenario, "history":history, "prompt_content":prompt_content
    }).to_string()
    
    print(f"Message content: {message_content}")
    try:
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": message_content,
                },
            ]
        )

        text = chat_response.choices[0].message.content
        return text
    except Exception as e:
        print(f"Error calling mistral api: {e}")
        return "This is an error message, something went wrong :("


