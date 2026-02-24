import os
import requests
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from utils.llm import safe_generate_content

# Force reload of environment variables
load_dotenv(override=True)

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ✅ Fetch Google search results via Serper.dev
def fetch_serper_results(query):
    if not SERPER_API_KEY:
        print("⚠️ SERPER_API_KEY not found. Skipping web search.")
        return []

    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    
    # Refine query for better results/efficiency
    payload = {"q": f"{query} market trends competitors 2024 2025"}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "organic" in data:
            return [
                f"{item['title']}. {item['snippet']}"
                for item in data["organic"][:3] 
                if "snippet" in item
            ]
        return []
    except Exception as e:
        print(f"❌ Serper error: {e}")
        return []

# ✅ Main market feedback agent
def market_feedback_agent(context, purpose, flow):
    if not SERPER_API_KEY:
        return "⚠️ Serper API key is missing. Market insights are limited to AI knowledge."

    # Use Purpose as primary search query for specificity
    query = purpose[:100] if purpose else context[:100]
    articles = fetch_serper_results(query)

    if not articles:
        return "⚠️ No real-time data found. Try refining your project goals for better search matching."

    if not GOOGLE_API_KEY:
        return "⚠️ GOOGLE_API_KEY missing. Cannot perform RAG for market insights."

    try:
        embedding = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=GOOGLE_API_KEY
        )

        docs = [Document(page_content=article) for article in articles]
        vectordb = Chroma.from_documents(docs, embedding)

        top_docs = vectordb.similarity_search(purpose, k=2)
        combined_refs = " | ".join([doc.page_content for doc in top_docs])
    except Exception as e:
        print(f"⚠️ Embedding/RAG error: {e}")
        combined_refs = " (Market data unavailable due to RAG switchover) "

    prompt = f"""
    You are the Market Intelligence Agent.
    
    COLLECTED INPUTS:
    - Vision: {purpose}
    - Proposed Flow: {flow}
    - Web Context: {combined_refs}

    TASK:
    1. Analyze how this project sits in the current 2024-2025 market.
    2. Suggest 3 specific features that would make this stand out.
    3. Identify 2 potential competitors or similar existing solutions.

    Format your response with clear bullet points (*) and bold headings for each point to ensure a professional report layout.
    """

    return safe_generate_content(prompt)
