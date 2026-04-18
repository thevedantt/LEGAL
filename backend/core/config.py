import os

class Config:
    LMSTUDIO_URL = os.getenv("LMSTUDIO_URL", "http://127.0.0.1:1234/v1/chat/completions")
    LMSTUDIO_MODEL = os.getenv("LMSTUDIO_MODEL", "mistral")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./tmp")
    
    LABEL_SET = [
        "Governing Law", "Termination", "Confidentiality", 
        "Indemnity", "Jurisdiction", "Payment", 
        "Obligations", "Other"
    ]

    RISK_RULES = {
        "Liability": "High",
        "Indemnity": "High",
        "Termination": "Medium",
        "Confidentiality": "Low"
    }

os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
