"""
Market Intelligence Agent
─────────────────────────
Uses LangChain's tool-calling pattern:
  1. Fetches live web search results via Serper.dev (Tool)
  2. Embeds + retrieves the most relevant snippets with Chroma (RAG)
  3. Invokes the LLM with the retrieved context (Generation)

This is a proper Retrieval-Augmented Generation (RAG) agent.
"""

import os
import requests
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from utils.llm import get_llm

load_dotenv(override=True)

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ── Tool: Web Search via Serper ────────────────────────────────────────────────
def _web_search(query: str, n: int = 5) -> list[str]:
    """Fetch top-n organic search snippets from Serper.dev."""
    if not SERPER_API_KEY:
        print("  [MarketAgent] SERPER_API_KEY missing – skipping web search.")
        return []
    try:
        resp = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
            json={"q": f"{query} market analysis 2025 competitors trends"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("organic", [])[:n]:
            title   = item.get("title", "")
            snippet = item.get("snippet", "")
            if snippet:
                results.append(f"{title}: {snippet}")
        return results
    except Exception as e:
        print(f"  [MarketAgent] Serper error: {e}")
        return []


# ── Tool: RAG retrieval ────────────────────────────────────────────────────────
def _rag_retrieve(documents: list[str], query: str, k: int = 3) -> str:
    """Embed documents, retrieve top-k relevant ones, return combined text."""
    if not documents:
        return ""
    if not GOOGLE_API_KEY:
        # Fallback: just concatenate all snippets
        return " | ".join(documents[:3])
    try:
        embedding = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=GOOGLE_API_KEY,
        )
        docs = [Document(page_content=d) for d in documents]
        vectordb = Chroma.from_documents(docs, embedding)
        top = vectordb.similarity_search(query, k=k)
        return " | ".join(d.page_content for d in top)
    except Exception as e:
        print(f"  [MarketAgent] RAG/Embedding error: {e}")
        return " | ".join(documents[:3])   # graceful fallback


# ── Prompt ─────────────────────────────────────────────────────────────────────
_SYSTEM = """You are the **Market Intelligence Agent** — an autonomous researcher
embedded in an AI planning pipeline. You have been given real-time web data.

Using the retrieved market data, produce a structured analysis:

## Market Position (2025)
[2-3 sentences: where does this project sit in today's landscape?]

## Standout Features (3 recommendations)
1. [Feature]: [Why it creates a competitive edge]
2. [Feature]: [Why it creates a competitive edge]
3. [Feature]: [Why it creates a competitive edge]

## Competitive Landscape
- Competitor 1: [Name] – [What they do, and what gap this project fills vs them]
- Competitor 2: [Name] – [What they do, and what gap this project fills vs them]

## Go-To-Market Insight
[One concrete GTM strategy recommendation based on the market data]

Use hyphens (-) for bullets, not unicode characters.
"""

_HUMAN = """Project Vision: {purpose}
Execution Flow Summary: {flow}
Retrieved Market Data: {market_data}

Generate the Market Intelligence report now."""

_prompt = ChatPromptTemplate.from_messages([("system", _SYSTEM), ("human", _HUMAN)])


# ── Main agent function ────────────────────────────────────────────────────────
def market_feedback_agent(context: str, purpose: str, flow: str) -> str:
    # Step 1: Web search
    search_query = (purpose or context)[:120]
    raw_docs = _web_search(search_query)

    # Step 2: RAG retrieval
    if raw_docs:
        market_data = _rag_retrieve(raw_docs, purpose)
    else:
        market_data = "No live web data available – analysis based on training knowledge only."

    # Step 3: LLM generation
    chain = _prompt | get_llm(temperature=0.4)
    result = chain.invoke({
        "purpose": purpose,
        "flow": flow[:500],          # keep prompt from exploding in size
        "market_data": market_data,
    })
    return result.content.strip()
