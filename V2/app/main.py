from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import shutil
import os
import numpy as np
from core.parser.pdf_parser import parse_pdf
from core.parser.docx_parser import parse_docx
from core.rag.chunking import chunk_text
from core.rag.embeddings import embed_texts
from core.rag.faiss_backend import build_faiss_index
from core.classifier.llm_classifier import classify_clause_llm
from core.risk.rule_based import rule_based_risk_flags
from core.risk.llm_risk import llm_risk_score
from core.summarizer.summarizer import summarize_contract_llm
from core.conflict.detector import detect_conflicts_rule_based, detect_conflicts_llm, all_clause_pairs
from core.qa.qa import answer_question

app = FastAPI()
UPLOAD_DIR = "./tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class TextRequest(BaseModel):
    contract_text: str
class QARequest(BaseModel):
    question: str
    contract_text: str

@app.post("/parse")
def parse_contract(file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        if file.filename.lower().endswith(".pdf"):
            text = parse_pdf(filepath)
        elif file.filename.lower().endswith(".docx"):
            text = parse_docx(filepath)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    return {"text": text[:10000]}

@app.post("/parse_txt")
def parse_txt_contract(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only TXT files supported")
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TXT parse error: {e}")
    return {"text": text[:10000]}

@app.get("/llm_health")
def llm_health():
    try:
        resp = classify_clause_llm("Test", health_check=True)
        if resp.get("error"): return {"ok": False, "detail": resp["error"]}
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "detail": str(e)}

@app.post("/rag/chunks")
def rag_chunks(payload: TextRequest):
    text = payload.contract_text
    chunks = chunk_text(text)
    return {"chunks": chunks}

@app.post("/classify")
def classify_endpoint(payload: TextRequest):
    text = payload.contract_text
    chunks = chunk_text(text)
    labeled = []
    for chunk in chunks:
        try:
            res = classify_clause_llm(chunk)
        except Exception as e:
            res = {"label": "Error", "reasoning": str(e)}
        labeled.append({"text": chunk, "label": res.get("label", "Error"), "reasoning": res.get("reasoning", "Error")})
    return {"clauses": labeled}

@app.post("/risk")
def risk_endpoint(payload: TextRequest):
    text = payload.contract_text
    chunks = chunk_text(text)
    risky = []
    for chunk in chunks:
        rules = rule_based_risk_flags(chunk)
        try:
            llm_score, llm_reason, raw = llm_risk_score(chunk)
        except Exception as e:
            llm_score, llm_reason = "Error", str(e)
        risky.append({"text": chunk, "rule_flags": rules, "llm_risk": llm_score, "llm_reasoning": llm_reason})
    return {"risks": risky}

@app.post("/summarize")
def summarize_endpoint(payload: TextRequest):
    text = payload.contract_text
    chunks = chunk_text(text)
    clause_infos = []
    try:
        for chunk in chunks:
            try:
                label = classify_clause_llm(chunk)
            except Exception as e:
                label = {"label": "Error", "reasoning": str(e)}
            
            rules = rule_based_risk_flags(chunk)
            
            try:
                llm_score, llm_reason, _ = llm_risk_score(chunk)
            except Exception as e:
                llm_score, llm_reason = "Error", str(e)
                
            clause_infos.append({
                "text": chunk, 
                "label": label.get("label", "Error"), 
                "classification_reasoning": label.get("reasoning",""), 
                "rule_risks": rules, 
                "risk": llm_score, 
                "risk_reasoning": llm_reason
            })
            
        result = summarize_contract_llm(text, clause_infos)
    except Exception as e:
        result = {"error": f"Summarization process failed: {str(e)}"}
        
    return {"summary": result}

@app.post("/conflicts")
def conflict_endpoint(payload: TextRequest):
    text = payload.contract_text
    chunks = chunk_text(text)
    rule_conf = detect_conflicts_rule_based(chunks)
    try:
        llm_conf = detect_conflicts_llm(all_clause_pairs(chunks, max_len=25))
    except Exception as e:
        llm_conf = [{"error": str(e)}]
    return {"rule_based_conflicts": rule_conf, "llm_conflicts": llm_conf}

@app.post("/qa")
def qa_endpoint(payload: QARequest):
    text = payload.contract_text
    if not text or len(text) < 20:
        raise HTTPException(status_code=400, detail="Contract text too short or missing.")
    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)
    index = build_faiss_index(np.array(embeddings))
    try:
        qa = answer_question(payload.question, chunks, index, embed_texts)
    except Exception as e:
        qa = {"answer": f"Backend Error: {str(e)}", "citations": []}
    return qa
