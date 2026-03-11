"""
Reviewer Agent
──────────────
Acts as a autonomous critic. Scores the plan and decides:
  - APPROVED  → pipeline proceeds to finalisation
  - REJECTED  → returns critique; pipeline loops back to re-plan

The critique text is injected into purpose_generator and flow_planner
on the next iteration so agents can self-correct.
"""

from langchain_core.prompts import ChatPromptTemplate
from utils.llm import get_llm

_SYSTEM = """You are the **Quality Assurance Critic Agent** in an autonomous AI planning pipeline.
Your verdict directly controls whether the pipeline loops for self-correction or proceeds.

Evaluation criteria (score each 1-5):
1. Alignment   – Does the execution flow actually fulfil the stated purpose?
2. Specificity – Are steps technical and concrete (not vague)?
3. Completeness– Are all lifecycle phases covered (design, build, test, deploy, monitor)?
4. Feasibility – Is the plan realistic for a real team?

Decision rules:
- If ALL criteria score >= 3: respond APPROVED
- Otherwise: respond REJECTED: [concise, actionable critique ≤ 100 words telling agents exactly what to fix]

⚠️ Your response MUST start with exactly "APPROVED" or "REJECTED:". No preamble.
"""

_HUMAN = """Project Context:
{context}

Strategic Purpose:
{purpose}

Execution Flow:
{flow}

Evaluate the plan now."""

_prompt = ChatPromptTemplate.from_messages([("system", _SYSTEM), ("human", _HUMAN)])


def review_plan(context: str, purpose: str, flow: str) -> str:
    chain = _prompt | get_llm(temperature=0.1)   # low temp for deterministic verdicts
    result = chain.invoke({"context": context, "purpose": purpose, "flow": flow})
    return result.content.strip()
