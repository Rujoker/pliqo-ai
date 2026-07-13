from fastapi import APIRouter, HTTPException
from models.schemas import AnalyzeRequest, AnalyzeResponse
from services.analyzer import analyze_document
import json

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    try:
        result = analyze_document(
            document=request.document,
            document_type=request.document_type,
            jurisdictions=request.jurisdictions,
            services=request.services
        )
        return AnalyzeResponse(**result)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI response")