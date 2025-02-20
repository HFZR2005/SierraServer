from typing import List, Dict

import random
import redis
import uuid
from fastapi import FastAPI, Response, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers.categorize_question import get_category 
from routers.scenario import create_scenario
from routers.conversational_child import get_child_response
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
    message: str



@app.get("/start-session", tags=["Start Session"])
async def start_session(response: Response):
    session_id = str(uuid.uuid4())
    redis_client.set(session_id, "active", ex=3600)
    response.set_cookie(key="session_id", value=session_id)
    return {"message": "access granted", "session_id": session_id}


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "THIS IS THE SIERRA PROJECT SERVER"}

'''
endpoints: 
/categorize-question (accepts a question in body with {question: ""}

/generate-response (for testing mode)

/generate-questions 
    (for practice mode - returns 4 question / stage 
    pairs which the user must reorder to the correct order as per protocol)

/give-feedback: 
    accepts a list of question, response pairs, 
    returns feedback on how effective the interviewer was at 
    conforming to Q types and staying within context
'''


@app.post("/categorize-question", tags=["Categorize Question"])
async def categorize_question(question: Dict[str, str]):
    # expecting {"question": ""}
    q = question["question"]
    category = get_category(q)
    
    return {"message": f"Question categorized as {category} THIS IS A TEST"}

@app.post("/generate-response", tags=["Generate Response"])
async def generate_response(question: Dict[str, str]):
    # expecting {"question": ""}
    return {"response": "Response generated"}

@app.get("/generate-questions", tags=["Generate Questions"])
async def generate_questions():
    return {"message": ["Question 1", "Question 2", "Question 3", "Question 4"]}

@app.post("/give-feedback", tags=["Give Feedback"])
async def give_feedback(responses: Dict[str, List[Dict[str, str]]]):
    # expecting {"questions": [{"question": "", "response": ""}, ...]}
    pairs = responses["questions"]
    is_correct = random.choice([True, False])
    return {"message": "Feedback generated", "is_correct": is_correct}


@app.get("/generate-scenario", tags=["Generate Scenario"])
async def generate_scenario():
    return create_scenario()

@app.get("/generate-question", tags=["Generate Question"])
async def generate_question():
    return {"question": "the question", "category": "the category"}


scenario = create_scenario()
scenario = scenario["Scenario"]

@app.post("/chat", tags=["Chat"])
async def chat(request: Request, message: ChatRequest):
    session_id = request.cookies.get("session_id")
    if not session_id:
        return {"message": "access denied"}

    history = redis_client.get(session_id)
    response = get_child_response(scenario, history, message.message)

    updated_history = f"{history}\n Interviewer: {message.message}\n You: {response}"
    redis_client.set(session_id, updated_history, ex=3600)

    return {"message": response}


