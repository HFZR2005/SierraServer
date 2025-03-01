
from typing import List, Dict

import random
import redis
import uuid
from fastapi import FastAPI, Response, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from tools.categorize_question import get_category 
from tools.scenario import create_scenario
from tools.conversational_child import get_child_response
from tools.generate_questions import generate_category_question, get_question_category
from pydantic import BaseModel 

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REDIS_HOST = "localhost"
REDIS_PORT = 6379

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

class ChatRequest(BaseModel):
    """
    Represents a chat request containing a scenario and a message.
    """
    scenario: str
    message: str

class Question(BaseModel):
    """
    Represents a question to be categorized.
    """
    question: str 


class QuestionResponse(BaseModel):
    """
    Represents a question-response pair.
    """
    question: str
    response: str


@app.get("/start-session", tags=["Start Session"])
async def start_session(response: Response) -> Dict[str, str]:
    """
    Starts a new user session and stores it in Redis.

    Args:
        response (Response): The response object to set the session cookie.

    Returns:
        dict: A message indicating access granted along with the session ID.
    """
    session_id = str(uuid.uuid4())
    redis_client.set(session_id, "active", ex=3600)
    response.set_cookie(key="session_id", value=session_id)
    return {"message": "access granted", "session_id": session_id}

@app.get("/", tags=["Root"])
async def read_root() -> Dict[str, str]:
    """
    Root endpoint for checking if the server is running.
    
    Returns:
        dict: A simple message indicating the server is active.
    """
    return {"message": "THIS IS THE SIERRA PROJECT SERVER"}

@app.post("/categorize-question", tags=["Categorize Question"])
async def categorize_question(question: Question) -> Dict[str, str]:
    """
    Categorizes a given question using the `get_category` function.
    
    Args:
        question (Question): The question to be categorized.
    
    Returns:
        dict: A message with the assigned category.
    """
    q = question.question
    category = get_category(q)
    
    return {"message": f"Question categorized as {category} THIS IS A TEST"}

@app.post("/give-feedback", tags=["Give Feedback"])
async def give_feedback(responses: Dict[str, List[QuestionResponse]]) -> Dict[str, bool]:
    """
    Provides feedback on user responses to questions.
    
    Args:
        responses (dict): A dictionary containing a list of question-response pairs.
    
    Returns:
        dict: A message with feedback and a randomly assigned correctness status.
    """
    pairs = responses["questions"]
    is_correct = random.choice([True, False])
    return {"message": "Feedback generated", "is_correct": is_correct}

@app.get("/generate-scenario", tags=["Generate Scenario"])
async def generate_scenario() -> Dict[str, str]:
    """
    Generates a scenario using the `create_scenario` function.
    
    Returns:
        dict: The generated scenario.
    """
    return create_scenario()

@app.get("/generate-question", tags=["Generate Question"])
async def generate_question() -> Dict[str, str]:
    """
    Generates a question and its category.
    
    Returns:
        dict: A generated question and its category.
    """

    category = get_question_category()
    question = generate_category_question(category)
    category = category.split(" ", 1)[0]

    return {"question": question, "category": category}

# Exception for when there is no session_id
class NoSession(Exception):
    """
    Exception raised when no session_id is found.
    """
    def __init__(self):
        super().__init__("No session_id found")

@app.post("/chat", tags=["Chat"])
async def chat(request: Request, message: ChatRequest) -> Dict[str, str]:
    """
    Handles user chat requests and interacts with the chatbot. Requires a session_id cookie. Sessions are valid for 1 hour.
    
    Args:
        request (Request): The HTTP request object to extract cookies.
        message (ChatRequest): The chat request containing a scenario and user message.
    
    Returns:
        dict: A response message from the chatbot.
    """
    try:
        session_id = request.cookies.get("session_id")
        if not session_id:
            raise NoSession 

        scenario = message.scenario
        history = redis_client.get(session_id)
        response = get_child_response(scenario, history, message.message)

        updated_history = f"{history}\n Interviewer: {message.message}\n You: {response}"
        redis_client.set(session_id, updated_history, ex=3600)

        return {"message": response}
    except Exception as e:
        return {"message": f"Error: {e.__str__()}"}


