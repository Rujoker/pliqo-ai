from fastapi import APIRouter
from models.schemas import ChatRequest, ChatResponse
from services.rag import retrieve, generate_answer

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    sources = retrieve(request.question)
    answer = generate_answer(request.question, request.document, sources)
    
    return ChatResponse(
        answer=answer,
        sources=[s["text"][:200] for s in sources]
    )