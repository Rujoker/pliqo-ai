import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def judge_answer(question: str, answer: str, expected_topics: list[str], sources: list[dict]) -> dict:
    sources_text = "\n".join([s["text"][:300] for s in sources])
    topics_text = ", ".join(expected_topics)

    prompt = f"""You are an expert evaluator for a legal compliance AI assistant.

Evaluate the following AI answer on three criteria. Return ONLY a JSON object, no markdown.

Question: {question}
Expected topics to cover: {topics_text}
Retrieved sources used:
{sources_text}

AI Answer:
{answer}

Evaluate on these criteria (score 0-10 each):

1. relevance: Does the answer directly address the question?
2. faithfulness: Is the answer grounded in the sources? No hallucinations?
3. coverage: Does the answer cover all expected topics?

Return this exact JSON:
{{
  "relevance": <0-10>,
  "faithfulness": <0-10>,
  "coverage": <0-10>,
  "overall": <average of three, rounded>,
  "passed": <true if overall >= 7>,
  "comment": "<one sentence explanation>"
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    return json.loads(raw)