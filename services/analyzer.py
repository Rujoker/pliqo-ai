from anthropic import Anthropic
from services.embeddings import get_chroma_client, get_collection
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def analyze_document(document: str, document_type: str, jurisdictions: list[str], services: list[str]) -> dict:
    chroma = get_chroma_client()
    collection = get_collection(chroma)

    results = collection.query(
        query_texts=[f"requirements for {document_type} {' '.join(jurisdictions)}"],
        n_results=3
    )
    context = "\n\n".join(results["documents"][0])

    prompt = f"""You are a legal compliance expert. Analyze the following {document_type} document and find compliance gaps.

Document to analyze:
{document if document else "[No document provided]"}

Services used: {', '.join(services) if services else 'none specified'}
Jurisdictions: {', '.join(jurisdictions) if jurisdictions else 'none specified'}

Relevant regulations:
{context}

Return a JSON object with this exact structure:
{{
  "score": <integer 0-100>,
  "summary": "<one sentence summary>",
  "findings": [
    {{
      "severity": "<critical|warning|info>",
      "title": "<short title>",
      "description": "<what is missing or wrong>",
      "recommendation": "<what to add or fix>",
      "reference": "<GDPR Art. X or CCPA Section Y>"
    }}
  ]
}}

Return only valid JSON, no markdown, no explanation."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text
    return json.loads(raw)