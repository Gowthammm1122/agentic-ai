"""
Context Reader Agent
────────────────────
Uses a LangChain prompt template + ChatGroq to extract a structured
project context from raw user inputs.
"""

from langchain_core.prompts import ChatPromptTemplate
from utils.llm import get_llm

_SYSTEM = """You are the **Context Extraction Agent** in a multi-agent AI planning system.
Your sole responsibility is to read raw user inputs and produce a crisp, structured
context summary that downstream agents will rely on.

Output format (use these exact section headers):
## Project Domain
[one sentence]

## Core Problem
[one to two sentences]

## Primary Users / Stakeholders
[bullet list]

## Key Constraints
[bullet list: time, budget, tech stack, regulations, etc.]

## Success Criteria
[bullet list of measurable outcomes]
"""

_HUMAN = """Title: {title}
Goals: {goals}
Specific Requirements / Notes: {feedback}

Extract and structure the project context now."""

_prompt = ChatPromptTemplate.from_messages([("system", _SYSTEM), ("human", _HUMAN)])


def context_reader(title: str, goals: str, feedback: str) -> str:
    chain = _prompt | get_llm(temperature=0.2)
    result = chain.invoke({"title": title, "goals": goals, "feedback": feedback or "None provided"})
    return result.content.strip()
