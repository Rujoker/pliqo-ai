from anthropic import Anthropic
from services.embeddings import get_chroma_client, get_collection
import os
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def retrieve(question: str, n_results: int = 3) -> list[dict]:
    chroma = get_chroma_client()
    collection = get_collection(chroma)
    
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )
    
    sources = []
    for i, doc in enumerate(results["documents"][0]):
        sources.append({
            "text": doc,
            "id": str(i)
        })
    
    return sources

def generate_answer(question: str, document: str, sources: list[dict]) -> str:
    context = "\n\n".join([s["text"] for s in sources])
    
    prompt = f"""You are a legal compliance assistant helping developers understand privacy law requirements.

User's document:
{document}

Relevant regulations:
{context}

Question: {question}

Answer based on the regulations above. Be specific, cite article numbers when relevant. If the document is missing something required by law, say so clearly."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text