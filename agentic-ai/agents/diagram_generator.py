"""
Diagram Generator Agent
───────────────────────
Converts the execution flow into a valid Mermaid flowchart.
Uses low temperature for syntactically consistent output.
"""

from langchain_core.prompts import ChatPromptTemplate
from utils.llm import get_llm

_SYSTEM = """You are the **Diagram Synthesis Agent**.
Convert an execution roadmap into a clean Mermaid LR flowchart.

Rules:
- Output ONLY the Mermaid code block — no explanation, no markdown headers.
- Use `flowchart LR` direction.
- Map each numbered step to a node: A[Step 1 label] --> B[Step 2 label] etc.
- Keep node labels short (max 5 words each).
- Group related steps into subgraphs if there are logical phases.
- Do NOT wrap in triple backticks.
"""

_HUMAN = """Execution Flow:
{flow}

Generate the Mermaid diagram now."""

_prompt = ChatPromptTemplate.from_messages([("system", _SYSTEM), ("human", _HUMAN)])


def generate_diagram(flow_steps: str) -> str:
    chain = _prompt | get_llm(temperature=0.1)
    result = chain.invoke({"flow": flow_steps})
    # Strip any accidental markdown fences the model might add
    raw = result.content.strip()
    for fence in ["```mermaid", "```"]:
        raw = raw.replace(fence, "")
    return raw.strip()
