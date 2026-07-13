from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str
    document: str = ""

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]

class AnalyzeRequest(BaseModel):
    document: str = ""
    document_type: str = "privacy_policy"
    jurisdictions: list[str] = ["gdpr"]
    services: list[str] = []

class Finding(BaseModel):
    severity: str
    title: str
    description: str
    recommendation: str
    reference: str

class AnalyzeResponse(BaseModel):
    score: int
    summary: str
    findings: list[Finding]