from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")

def generate_feedback(context, purpose, flow):
    prompt = f"""
You are an expert project reviewer.

Review the following project:

Context Summary:
{context}

Purpose Statement:
{purpose}

Process Flow:
{flow}

Provide helpful, constructive feedback on clarity, feasibility, and areas to improve.
"""

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
