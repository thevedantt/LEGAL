from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import shutil
import numpy as np

from services.parser_service import ParserService
from services.inference_service import InferenceService
from services.rag_service import RAGService
from services.risk_analyzer import RiskAnalyzer
from services.summarizer_service import SummarizerService
from services.conflict_service import ConflictService
from core.config import Config

router = APIRouter()
inference_service = InferenceService()
rag_service = RAGService()
risk_analyzer = RiskAnalyzer()
summarizer_service = SummarizerService()
conflict_service = ConflictService()

class TextRequest(BaseModel):
    contract_text: str

class QARequest(BaseModel):
    question: str
    context: str = None
    contract_text: str = None

@router.post("/parse")
async def parse_contract(file: UploadFile = File(...)):
    filepath = os.path.join(Config.UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        if file.filename.lower().endswith(".pdf"):
            text = ParserService.parse_pdf(filepath)
        elif file.filename.lower().endswith(".docx"):
            text = ParserService.parse_docx(filepath)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze_contract(payload: TextRequest):
    chunks = rag_service.chunk_text(payload.contract_text)
    analysis = []
    for chunk in chunks[:10]: # Limit for demo
        res = inference_service.analyze_clause(chunk)
        analysis.append(res)
    return {"analysis": analysis}

@router.post("/risk")
async def risk_assessment(payload: TextRequest):
    chunks = rag_service.chunk_text(payload.contract_text)
    risks = []
    for chunk in chunks[:10]:
        score, reason = risk_analyzer.llm_risk_score(chunk)
        rules = risk_analyzer.rule_based_risk_flags(chunk)
        risks.append({"text": chunk, "score": score, "reason": reason, "rule_flags": rules})
    return {"risks": risks}

@router.post("/summarize")
async def summarize_contract(payload: TextRequest):
    # For summarization, we need some classified info first
    chunks = rag_service.chunk_text(payload.contract_text)
    clause_infos = []
    for chunk in chunks[:15]:
        res = inference_service.analyze_clause(chunk)
        score, reason = risk_analyzer.llm_risk_score(chunk)
        clause_infos.append({
            "text": chunk,
            "label": res["label"],
            "risk": score,
            "reasoning": reason
        })
    
    summary = summarizer_service.summarize(payload.contract_text, clause_infos)
    return summary

@router.post("/conflicts")
async def detect_conflicts(payload: TextRequest):
    chunks = rag_service.chunk_text(payload.contract_text)
    rule_conflicts = conflict_service.detect_rule_based(chunks)
    
    # LLM conflicts can be slow, so we take a sample of pairs
    pairs = conflict_service.get_clause_pairs(chunks, max_len=10)
    llm_conflicts = conflict_service.detect_llm(pairs)
    
    return {
        "rule_based_conflicts": rule_conflicts,
        "llm_conflicts": llm_conflicts
    }

@router.post("/qa")
@router.post("/api/v1/ask")
async def qa_endpoint(payload: QARequest):
    context = payload.context or payload.contract_text
    if not context:
        raise HTTPException(status_code=400, detail="Missing context or contract_text")
    
    answer = rag_service.rag_pipeline(
        query=payload.question, 
        context=context, 
        llm_client=inference_service.client
    )
    
    return {"answer": answer}
