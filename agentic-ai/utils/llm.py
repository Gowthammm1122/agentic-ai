"""
LLM utility – returns a LangChain ChatGroq instance.

All agents use this single entry-point so it's easy to swap models.
"""

import os
import time
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

# ── Model config ───────────────────────────────────────────────────────────────
PRIMARY_MODEL  = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
FALLBACK_MODEL = "llama-3.3-70b-versatile"


def get_llm(model: str | None = None, temperature: float = 0.4) -> ChatGroq:
    """Return a configured ChatGroq instance."""
    return ChatGroq(
        model=model or PRIMARY_MODEL,
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=temperature,
        max_retries=2,
    )


def safe_invoke(prompt: str, temperature: float = 0.4, max_retries: int = 3) -> str:
    """
    Invoke the LLM with automatic retry + model fallback.
    Returns the response text, or an error message on total failure.
    """
    models_to_try = [PRIMARY_MODEL, FALLBACK_MODEL]
    delay = 2

    for model_name in models_to_try:
        llm = get_llm(model=model_name, temperature=temperature)
        for attempt in range(max_retries):
            try:
                response = llm.invoke([HumanMessage(content=prompt)])
                return response.content.strip()
            except Exception as e:
                err = str(e).lower()
                if "rate limit" in err or "429" in err:
                    if attempt < max_retries - 1:
                        print(f"  [LLM] Rate-limit hit ({model_name}). Waiting {delay}s …")
                        time.sleep(delay)
                        delay *= 2
                        continue
                if "not found" in err or "unsupported" in err or "model" in err:
                    print(f"  [LLM] Model '{model_name}' unavailable – trying fallback.")
                    break          # skip to next model in list
                print(f"  [LLM] Error: {e}")
                break

    return "[LLM unavailable – check GROQ_API_KEY and model name]"


# Backwards-compat alias used by older agent files
def safe_generate_content(prompt: str, **_kwargs) -> str:
    return safe_invoke(prompt)
