from typing import List, Dict

import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.categorize_question import get_category 

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/generate-response", tags=["Generate Response"])
async def generate_response():
    return {"message": "Response generated"}

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
    return {"message": "Scenario generated"}



