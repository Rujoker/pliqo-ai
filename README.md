# Pliqo AI

AI-powered legal document analysis backend for [Pliqo](https://pliqo.vercel.app) - a privacy policy generator for developers.

Built to demonstrate production-ready AI engineering practices: RAG pipeline, agentic document analysis, and LLM evaluation harness.

## What it does

- **RAG Q&A** - answer questions about GDPR/CCPA compliance based on a regulatory corpus
- **Document Analyzer** - agent that audits a privacy policy and returns structured findings with severity levels and article references
- **Document Upload** - analyze an existing PDF or text document for compliance gaps
- **Eval Harness** - LLM-as-judge evaluation pipeline with golden dataset and coverage scoring

## Tech stack

- Python 3.12, FastAPI, Pydantic
- ChromaDB (vector store, persistent local)
- Anthropic Claude (claude-sonnet-4-6)
- pytest-compatible eval runner

## Architecture
Request → FastAPI Router → Service Layer → ChromaDB (retrieval) + Claude (generation) → Response
↓
Eval Harness (offline, LLM-as-judge)

## Quick start

```bash
git clone https://github.com/your-username/pliqo-ai
cd pliqo-ai

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

python services/embeddings.py  # index corpus
uvicorn main:app --reload
```

## API

### POST /api/chat
RAG-based Q&A about compliance.

```json
{
  "question": "Do I need to mention the right to erasure?",
  "document": "optional: paste your current policy here"
}
```

### POST /api/analyze
Agent that audits a document and returns findings.

```json
{
  "document": "We collect your email...",
  "document_type": "privacy_policy",
  "jurisdictions": ["gdpr"],
  "services": ["stripe", "firebase"]
}
```

### POST /api/upload
Upload a PDF or .txt file for analysis.

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@privacy_policy.pdf" \
  -F "jurisdictions=gdpr" \
  -F "services=stripe"
```

## Eval harness

```bash
python eval/run_eval.py
```

Runs 5 golden dataset cases through the RAG pipeline, scores each with an LLM-as-judge on relevance, faithfulness, and coverage. Results saved to `eval/results/`.

Latest run: 5/5 passed, average score 8.0/10.

Key finding: faithfulness scores (5-6/10) reveal the model draws on parametric knowledge beyond the retrieved corpus - a signal to expand the corpus rather than a prompt issue.

## Live API

Base URL: `https://web-production-7869b.up.railway.app`

- `GET /health`
- `POST /api/chat`
- `POST /api/analyze`
- `POST /api/upload`