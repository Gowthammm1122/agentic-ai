"""
Purpose Generator Agent
───────────────────────
Reads the structured context + any reviewer critique from a previous
rejection and produces (or refines) a high-level project purpose statement.
"""

from langchain_core.prompts import ChatPromptTemplate
from utils.llm import get_llm

_SYSTEM = """You are the **Strategic Vision Agent** inside a self-correcting AI planner.
Your job is to craft a compelling, concrete Project Purpose statement.

Rules:
- Be visionary but grounded — avoid vague platitudes.
- Include WHY this project matters, WHO it helps, and WHAT measurable change it drives.
- If a reviewer has previously rejected a plan, incorporate their critique to improve this iteration.
- Length: 3–5 focused paragraphs. No bullet lists — this is a narrative vision statement.
"""

_HUMAN = """Project Title: {title}
Structured Context: {context}
Reviewer Critique (if any): {critique}

Write the Strategic Purpose statement now."""

_prompt = ChatPromptTemplate.from_messages([("system", _SYSTEM), ("human", _HUMAN)])


def generate_purpose(context: str, title: str, critique: str = "") -> str:
    chain = _prompt | get_llm(temperature=0.5)
    result = chain.invoke({"title": title, "context": context, "critique": critique or "None – first attempt."})
    return result.content.strip()
