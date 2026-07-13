from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str
    document: str = ""

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]