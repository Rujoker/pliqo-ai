import pytest
from pydantic import ValidationError

from models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    ChatRequest,
    ChatResponse,
    Finding,
)


def test_chat_request_requires_question():
    with pytest.raises(ValidationError):
        ChatRequest()  # question is required


def test_chat_request_document_defaults_to_empty():
    req = ChatRequest(question="Do I need a cookie banner?")
    assert req.document == ""


def test_chat_response_contract():
    resp = ChatResponse(answer="Yes.", sources=["GDPR Art. 7"])
    assert resp.answer == "Yes."
    assert resp.sources == ["GDPR Art. 7"]


def test_analyze_request_defaults():
    req = AnalyzeRequest(document="We collect your email...")
    assert req.document_type == "privacy_policy"
    assert req.jurisdictions == ["gdpr"]
    assert req.services == []


def test_analyze_response_nests_findings():
    finding = Finding(
        severity="high",
        title="Missing right to erasure",
        description="The policy does not mention data deletion.",
        recommendation="Add a section describing how users can request erasure.",
        reference="GDPR Art. 17",
    )
    resp = AnalyzeResponse(score=72, summary="Mostly compliant.", findings=[finding])

    assert resp.score == 72
    assert resp.findings[0].reference == "GDPR Art. 17"


def test_finding_requires_all_fields():
    with pytest.raises(ValidationError):
        Finding(severity="low", title="Incomplete")  # missing required fields