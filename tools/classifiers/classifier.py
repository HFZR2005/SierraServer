from transformers import BertForSequenceClassification
from transformers import AutoTokenizer 
import torch


qtype_path = 'tools/classifiers/q_type'
stage_path = 'tools/classifiers/stage'
model_qtype = BertForSequenceClassification.from_pretrained(qtype_path)
model_stage = BertForSequenceClassification.from_pretrained(stage_path)
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
labels_qtype = {1: "Open-ended", 2: "Directive", 3: "Option Posing", 4: "Suggestive"}
labels_stage = {1: "Introduction", 2: "Investigation stage", 3: "Closing phase"}
    

def get_question_type(question) -> tuple[str, float]:
    encoding = tokenizer(question, return_tensors="pt", truncation=True, padding='max_length')
    with torch.no_grad():
        output = model_qtype(**encoding)
    logits = output.logits 
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    prediction = torch.argmax(probabilities, dim=-1).item()
    confidence = probabilities[0, prediction].item()
    return (labels_qtype[prediction], confidence)


def get_stage(question) -> tuple[str, float]:
    encoding = tokenizer(question, return_tensors="pt", truncation=True, padding='max_length')
    with torch.no_grad():
        output = model_stage(**encoding)
    logits = output.logits 
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    prediction = torch.argmax(probabilities, dim=-1).item()
    confidence = probabilities[0, prediction].item()
    return (labels_stage[prediction], confidence)
