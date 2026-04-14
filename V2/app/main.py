from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
from core.parser.pdf_parser import parse_pdf
from core.parser.docx_parser import parse_docx

app = FastAPI()

UPLOAD_DIR = "./tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
    return {"text": text[:10000]}  # Return max 10k chars for now
