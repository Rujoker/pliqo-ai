from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from models.schemas import AnalyzeResponse
from services.parser import extract_text
from services.analyzer import analyze_document
import json

router = APIRouter()

@router.post("/upload", response_model=AnalyzeResponse)
async def upload(
    file: UploadFile = File(...),
    document_type: str = Form(default="privacy_policy"),
    jurisdictions: str = Form(default="gdpr"),
    services: str = Form(default="")
):
    try:
        file_bytes = await file.read()
        document = extract_text(file.filename, file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to parse file")

    jurisdictions_list = [j.strip() for j in jurisdictions.split(",") if j.strip()]
    services_list = [s.strip() for s in services.split(",") if s.strip()]

    try:
        result = analyze_document(
            document=document,
            document_type=document_type,
            jurisdictions=jurisdictions_list,
            services=services_list
        )
        return AnalyzeResponse(**result)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI response")