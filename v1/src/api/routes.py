from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.inference_service import InferenceService

router = APIRouter()
service = InferenceService()

class AnalyzeRiskRequest(BaseModel):
    clause: str

class AskRequest(BaseModel):
    question: str
    context: str

class SummarizeRequest(BaseModel):
    text: str

@router.post("/analyze-risk")
def analyze_risk(request: AnalyzeRiskRequest):
    try:
        result = service.analyze_clause(request.clause)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask")
def ask_question(request: AskRequest):
    try:
        prompt = f"""
You are a legal assistant. Answer the question based on the provided contract context.

Context: {request.context}

Question: {request.question}

Answer:
"""
        answer = service.client.generate(prompt)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize")
def summarize_contract(request: SummarizeRequest):
    try:
        prompt = f"""
Summarize the following contract text in a concise manner, highlighting key terms and obligations.

Contract: {request.text}

Summary:
"""
        summary = service.client.generate(prompt)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))