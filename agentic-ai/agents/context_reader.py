# agents/context_reader.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def context_reader(project_title, user_goals, feedback_notes):
    prompt = f"""
You are an AI that helps summarize student project goals and feedback.

Project Title: {project_title}
User Goals: {user_goals}
User Feedback: {feedback_notes}

Summarize the user needs, pain points, and opportunity areas in bullet points.
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"
