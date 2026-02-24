import time
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_groq_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

# The model user requested. Fallback to llama if it fails.
DEFAULT_MODEL = "openai/gpt-oss-120b"
FALLBACK_MODEL = "llama-3.3-70b-versatile"

def safe_generate_content(prompt, model_name=None, max_retries=3, initial_delay=2):
    """
    Wrapper for Groq API with exponential backoff.
    """
    current_model = model_name or os.getenv("GROQ_MODEL", DEFAULT_MODEL)
    delay = initial_delay
    client = get_groq_client()

    for attempt in range(max_retries):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=current_model,
            )
            return chat_completion.choices[0].message.content.strip()
        
        except Exception as e:
            error_msg = str(e).lower()
            
            # Check for Rate Limit (429)
            if "rate limit" in error_msg or "429" in error_msg:
                if attempt < max_retries - 1:
                    print(f"⚠️ Groq Rate limit hit. Retrying in {delay}s...")
                    time.sleep(delay)
                    delay *= 2
                    continue
            
            # Check for invalid model error (common if the requested model doesn't exist on Groq)
            if "not found" in error_msg or "unsupported" in error_msg:
                if current_model != FALLBACK_MODEL:
                    print(f"⚠️ Model {current_model} not found on Groq. Falling back to {FALLBACK_MODEL}...")
                    current_model = FALLBACK_MODEL
                    delay = initial_delay # reset delay for new model
                    continue

            print(f"❌ Groq Error: {e}")
            break
            
    return "⚠️ Groq is currently unavailable or the model name is incorrect. Please check your API key and model name."
