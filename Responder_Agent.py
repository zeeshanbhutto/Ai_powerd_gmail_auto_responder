# responder_agent.py

import ollama  # If you’re using Ollama locally
from prompt_templates import reply_prompt

import ollama

def generate_reply(subject, body):
    prompt = f"You received an email with subject: '{subject}' and body:\n\n{body}\n\nWrite a concise and professional reply."
    response = ollama.chat(
        model="gemma2:2b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']


def classify_email(subject, body, model="gemma2:2b"):
    prompt = f"Classify the following email into one of these categories: Job, Internship, Newsletter, Promotion, Other.\n\nSubject: {subject}\n\nBody: {body}"
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content'].strip()
