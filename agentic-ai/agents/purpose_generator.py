# agents/purpose_generator.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def generate_purpose_statement(context_summary):
    prompt = f"""
You are an AI that writes clear project purpose statements.

Based on the context:
---
{context_summary}
---

Write in this format:
"My product/app will help [audience] with [problem] by [solution]."
Only output the sentence.
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"
