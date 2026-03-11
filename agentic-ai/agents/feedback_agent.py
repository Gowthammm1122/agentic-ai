"""
Feedback / Risk Assessment Agent
─────────────────────────────────
Produces a structured technical risk review — the "Senior Engineer" voice
that challenges the plan before it goes to export.
"""

from langchain_core.prompts import ChatPromptTemplate
from utils.llm import get_llm

_SYSTEM = """You are the **Senior Technical Analyst Agent** — the most experienced engineer
in this autonomous planning system. Your role is to stress-test the plan,
not rubber-stamp it.

Output format (use these exact section headers, each with 2-3 bullet points):

## Critical Risks
[What could cause this project to fail? Be specific.]

## Missing Components
[Identify any gaps in the execution flow — things skipped or underspecified.]

## Technical Optimisations
[Concrete suggestions to make the implementation faster, cheaper, or more robust.]

## Recommended Monitoring Metrics
[What KPIs / metrics should the team track post-launch?]

Be direct. Use hyphens (-) for bullets, not unicode characters.
"""

_HUMAN = """Project Context: {context}
Strategic Purpose: {purpose}
Execution Flow: {flow}

Provide your expert critique now."""

_prompt = ChatPromptTemplate.from_messages([("system", _SYSTEM), ("human", _HUMAN)])


def generate_feedback(context: str, purpose: str, flow: str) -> str:
    chain = _prompt | get_llm(temperature=0.3)
    result = chain.invoke({"context": context, "purpose": purpose, "flow": flow})
    return result.content.strip()
