from transformers import BertForSequenceClassification
from transformers import AutoTokenizer 
import torch


path = 'tools/classifiers/q_type'
model = BertForSequenceClassification.from_pretrained(path)
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
labels = {1: "Open-ended", 2: "Directive", 3: "Option Posing", 4: "Suggestive"}
    

def get_question_type(question):
    encoding = tokenizer(question, return_tensors="pt", truncation=True, padding='max_length')
    with torch.no_grad():
        output = model(**encoding)
    logits = output.logits 
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    prediction = torch.argmax(probabilities, dim=-1).item()
    confidence = probabilities[0, prediction].item()
    return (labels[prediction], confidence)
