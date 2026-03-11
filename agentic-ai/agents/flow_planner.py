"""
Flow Planner Agent
──────────────────
Produces a numbered, technical execution roadmap.
Aware of reviewer feedback so it can self-correct on rejection.
"""

from langchain_core.prompts import ChatPromptTemplate
from utils.llm import get_llm

_SYSTEM = """You are the **Execution Architect Agent** in a multi-agent AI planning system.
Your task is to translate a strategic vision into a concrete, numbered execution roadmap.

Rules:
- Produce exactly 8–12 numbered steps.
- Each step must follow the format:   N. [Phase Name]: [Action Description]
- Steps must be ordered logically: discovery → design → build → test → deploy → monitor.
- Be technical and specific. Avoid generic steps like "Plan the project."
- If reviewer critique is provided, fix the weaknesses they identified.
"""

_HUMAN = """Strategic Purpose: {purpose}
Project Context: {context}
Reviewer Critique (if any): {critique}

Generate the Execution Roadmap now."""

_prompt = ChatPromptTemplate.from_messages([("system", _SYSTEM), ("human", _HUMAN)])


def plan_flow(purpose: str, context: str, critique: str = "") -> str:
    chain = _prompt | get_llm(temperature=0.4)
    result = chain.invoke({"purpose": purpose, "context": context, "critique": critique or "None – first attempt."})
    return result.content.strip()
