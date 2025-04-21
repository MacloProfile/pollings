import json

with open('questions.json', 'r', encoding='utf-8-sig') as f:
    QUESTIONS = json.load(f)['Questions']
