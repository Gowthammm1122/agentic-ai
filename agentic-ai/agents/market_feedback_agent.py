import os
import requests
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
import google.generativeai as genai

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ Fetch Google search results via Serper.dev
def fetch_serper_results(query):
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        if "organic" in data:
            return [
                f"{item['title']}. {item['snippet']}"
                for item in data["organic"][:5]
                if "snippet" in item
            ]
        return []
    except Exception as e:
        print("❌ Serper error:", e)
        return []

# ✅ Main market feedback agent
def market_feedback_agent(context, purpose):
    query = purpose or context or "AI tools for students"
    articles = fetch_serper_results(query)

    if not articles:
        return "⚠️ Could not fetch Serper data. Check your API key or try a broader query."

    embedding = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    docs = [Document(page_content=article) for article in articles]
    vectordb = Chroma.from_documents(docs, embedding, collection_name="serper_rag")

    top_docs = vectordb.similarity_search(purpose, k=2)
    combined_refs = " | ".join([doc.page_content for doc in top_docs])

    prompt = f"""
    Context: {context}
    Purpose: {purpose}
    Real-time Web Context: {combined_refs}

    Based on this, provide market-aligned suggestions, insights, competitor ideas, or feature improvements.
    """

    response = model.generate_content(prompt)
    return response.text.strip()
