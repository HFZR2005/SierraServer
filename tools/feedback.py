import os
from mistralai import Mistral
import os
from dotenv import load_dotenv
from typing import Dict
from langchain_core.prompts import PromptTemplate

from typing import List
from numpy import float64 

from scipy.spatial import distance 
from sentence_transformers import SentenceTransformer

THRESHOLD = 0.85
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')


class InvalidQAQError(Exception):
    """
    Exception for when the QAQ list is not of length 3.
    """
    # message for the exception 

    def __init__(self, message):
        super().__init__(message)


def calculate_similarity(QAQ: List[str]) -> float:
    if len(QAQ) == 3:
        q1, a, q2 = QAQ
        q1_embedding = sentence_model.encode(q1)
        q2_embedding = sentence_model.encode(q2)
        a_embedding = sentence_model.encode(a)


        # calculate score between q2 and q1 and if its too small, q2 and a 
        score = max(1, (1 - distance.cosine(q1_embedding, q2_embedding)) / THRESHOLD)
        if score < 0.2:
            score = max(1, (1 - distance.cosine(a_embedding, q2_embedding)) / THRESHOLD)
        return float(score)
    else:
        raise InvalidQAQError("QAQ list must be of length 3")


def calculate_score(QResponseList: List[str]) -> float:
    if len(QResponseList) < 3:
        raise InvalidQAQError("QAQ list must be of length 3")
    else: 
        total = 0
        count = 0

        for i in range(2, len(QResponseList)):
            QAQ = [QResponseList[i-2], QResponseList[i-1], QResponseList[i]]
            score = calculate_similarity(QAQ)
            total += score 
            count += 1
        
        mean = total/count 
        return float(mean) 



