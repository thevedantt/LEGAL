import requests
import os
import json

LMSTUDIO_URL = os.getenv("LMSTUDIO_URL", "http://127.0.0.1:1234/v1/chat/completions")
MODEL_NAME = os.getenv("LMSTUDIO_MODEL", "mistral")

SUMMARY_SCHEMA = """
Return a JSON summarizing the contract:
{
  "parties": [list of named parties involved],
  "effective_date": <effective date string or null>,
  "duration": <duration or null>,
  "key_clauses": [
    {"label": <clause type>, "text": <clause>, "risk": <risk rating>, "reasoning": <risk reasoning>}
  ],
  "top_risks": [<summary of main risks with reasoning>],
  "notable_conflicts": [<conflicts if found>],
  "summary": <plain English overall summary>
}
"""

def summarize_contract_llm(contract_text, clause_infos, url=LMSTUDIO_URL, model=MODEL_NAME):
    """
    contract_text: long string (parsed treaty)
    clause_infos: list[{"label":..., "text":..., "risk":..., "reasoning":...}]
    returns: dict summary (parsed from JSON output of LLM)
    """
    context = "\n".join([f"Clause: {ci['text']}\nType: {ci['label']}\nRisk: {ci.get('risk','')}\nReasoning: {ci.get('reasoning','')}" for ci in clause_infos])
    prompt = f"{SUMMARY_SCHEMA}\nContract begins:\n{contract_text[:4000]}\n\nKey extracted clauses and risk info:\n{context}\n"
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 2000,
    }
    resp = requests.post(url, json=body)
    if not resp.ok:
        raise RuntimeError(f"LLM summarization failed: {resp.status_code} {resp.text}")
    raw = resp.json()["choices"][0]["message"]["content"].strip()
    # Try to extract JSON
    try:
        first_brace = raw.find('{')
        if first_brace != -1:
            raw = raw[first_brace:]
        summary = json.loads(raw)
    except Exception:
        summary = {"error": "Could not parse summary as JSON", "raw": raw}
    return summary
