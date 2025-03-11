from typing import List, Dict 
import redis
import uuid
from fastapi import FastAPI, Response, Request 
from fastapi.middleware.cors import CORSMiddleware
from tools.scenario import create_scenario
from tools.conversational_child import get_child_response
from tools.classifiers.classifier import get_question_type, get_stage
from tools.classifiers.LLM_classifier import LLM_get_question_type, LLM_get_stage
from tools.generate_questions import LLM_generate_question, get_question_category
from tools.feedback import calculate_score
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


@app.post("/end-stage-feedback", tags=["Give End-Stage Feedback"])
async def give_feedback(responses: Dict[str, List[QuestionResponse]]) -> Dict[str, int]:
    """
    Provides feedback on user responses to questions.
    
    Args:
        responses (dict): A dictionary containing a list of question-response pairs.
    
    Returns:
        dict: A score indicating the quality of the responses. 
    """
    # have QAQAQAQA 
    QAQList = []
    for i, pair in enumerate(responses["responses"]):
        if i == len(responses["responses"]) - 1:
            QAQList.append(pair.question)
        else:
            QAQList.append(pair.question)
            QAQList.append(pair.response)

    score = float(calculate_score(QAQList))

    score = int(10 * score)
    return {"score": score}

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
    question = LLM_generate_question(category)
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
        if not history:
            history = ""
        response = get_child_response(scenario, history, message.message)

        updated_history = f"{history}\n Interviewer: {message.message}\n You: {response}"
        redis_client.set(session_id, updated_history, ex=3600)

        return {"message": response}
    except Exception as e:
        return {"message": f"Error: {e.__str__()}"}

@app.post("/llm-categorize-question")
async def llm_categorize_question(question: Question) -> Dict[str, str]:
    """
    Used as a backup to our finetuned classifier for when it is unsure.

    Args:
        question: Question to be classified

    Returns:
        dict: category that question has been determined as
    """

    q_type = LLM_get_question_type(question.question)
    return {"question_type": q_type}


@app.post("/live-feedback", tags=["Live Feedback"])
async def generate_test_feedback(messages: Dict[str, str]) -> Dict[str, tuple[str, float] | bool]: 
    """
    Generates feedback on questions asked by the user in the testing section. Includes whether
    the question is the correct type, the correct stage, and that there has been no context jump.

    Args:
        messages: a triple containing question, response, question

    Returns:
        dict: Question type, stage and whether a switch in context has been detected.
    """
    
    Q1, A1, Q2 = messages["question_1"], messages["response"], messages["question_2"] 
    q_type = get_question_type(Q1) 
    q_stage = get_stage(Q1)
    context_switch_score = calculate_score([Q1, A1, Q2]) 
    context_switch = context_switch_score < 0.3

    return {"q_type": q_type, "q_stage" : q_stage, "context_switch": context_switch}


@app.post("/categorize-question", tags=["Get Question Type"])
async def q_type_categorize(question: Question):
    """ 
    Categorises a question into one of the 4 categories:
        Open-Ended, Directive, Option-Posing, Suggestive

    Args: 
        question: Question to be classified.

    Returns:
        dict: Question type and the confidence level of the classifier.
    """
    q_type, confidence = get_question_type(question.question)
    return {"question_type": q_type, "confidence": confidence}

@app.post("/categorise-stage", tags=["Get Question Stage"])
def categorise_stage(question: Question) -> Dict[str, str]:
    """
    Categorises a question into one of the stages using an LLM (backup for trained classifier):
        Introduction, Investigative, Closing

    Args:
        question: Question to be classifed into a stage.

    Returns:
        dict: Stage
    """
    return {"stage": LLM_get_stage(question.question)}



@app.post("/categorize-question-stage", tags=["Get Question Stage"])
async def q_stage_categorize(question: Question):
    """ 
    Categorises a question into one of the 3 stage categories:
        Introduction, Investigation stage, Closing stage

    Args: 
        question: Question to be classified.

    Returns:
        dict: Question stage and the confidence level of the classifier.
    """
    q_stage, confidence = get_stage(question.question)
    return {"question_type": q_stage, "confidence": confidence}
