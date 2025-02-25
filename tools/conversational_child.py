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
    You are a child being questioned for evidence of a crime that has happened against you. Your role is to respond **authentically as a child** in the given scenario.

    ### Scenario:
    {scenario}

    ### Conversation History:
    {history}

    The interviewer says:
    **"{prompt_content}"**

    **Your task:**
    - **Stay in character** as a child in the given scenario.
    - **Respond naturally and consistently** with the scenario.
    - **Only provide dialogue** (no descriptions, emotions, or actions).
    
    **You respond:**
    """
)

def get_child_response(scenario, history, prompt_content):
    """
    Generates a chatbot response based on the given scenario, conversation history, and prompt content.

    Args:
        scenario (str): The specific context or scenario for the chatbot.
        history (list): A list containing previous messages in the conversation.
        prompt_content (str): The main content or user query for generating a response.

    Returns:
        str: The chatbot's response text or an error message if the API call fails.
    """    

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


