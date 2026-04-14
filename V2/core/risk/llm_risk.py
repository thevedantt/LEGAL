import requests
import os

LMSTUDIO_URL = os.getenv("LMSTUDIO_URL", "http://127.0.0.1:1234/v1/chat/completions")
MODEL_NAME = os.getenv("LMSTUDIO_MODEL", "mistral")

def llm_risk_score(clause, url=LMSTUDIO_URL, model=MODEL_NAME):
    """
    Asks LLM to evaluate risk of a clause. Returns (risk_level, risk_reasoning, raw answer)
    """
    prompt = f"""Assess the following contract clause for risk to our company. Answer only in this format:
Risk:[High|Medium|Low]\nReasoning:<one-sentence explanation>\n
Clause: {clause}"
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "max_tokens": 150
    }
    response = requests.post(url, json=body)
    if not response.ok:
        return ("Unknown", "LLM API error", response.text)
    raw = response.json()["choices"][0]["message"]["content"].strip()
    risk, reasoning = "Unknown", "No reasoning returned."
    for line in raw.split("\n"):
        if line.lower().startswith("risk:"):
            val = line.split(":", 1)[1].strip().lower()
            if val.startswith("high"): risk = "High"
            elif val.startswith("medium"): risk = "Medium"
            elif val.startswith("low"): risk = "Low"
        if line.lower().startswith("reasoning:"):
            reasoning = line.split(":", 1)[1].strip()
    return (risk, reasoning, raw)
