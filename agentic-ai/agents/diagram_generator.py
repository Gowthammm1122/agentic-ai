import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def generate_mermaid_diagram(process_flow_text):
    prompt = f"""
You are an expert in turning project plans into diagrams.

Convert this project milestone plan into a MermaidJS flowchart:

{process_flow_text}

Use the format:

graph TD
  M1["Milestone 1: ..."]
  T1["Task 1"]
  M1 --> T1

Only return the raw Mermaid code.
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error: {e}"
