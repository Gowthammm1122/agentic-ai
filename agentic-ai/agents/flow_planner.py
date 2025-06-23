import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def generate_project_flow(purpose_statement):
    prompt = f"""
You are an expert project planner.

Given this purpose statement:
"{purpose_statement}"

Break the project down into 4–6 major milestones.
Each milestone should have 2–3 clear, actionable tasks.

Respond in a clean bullet-point format, grouped by milestone.
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"
