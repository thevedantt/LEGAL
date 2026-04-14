import requests
import os

LMSTUDIO_URL = os.getenv("LMSTUDIO_URL", "http://127.0.0.1:1234/v1/chat/completions")
MODEL_NAME = os.getenv("LMSTUDIO_MODEL", "mistral")

FEW_SHOT_EXAMPLES = """
Classify the clause type.

Clause: "This Agreement is governed by the laws of England."
Label: Governing Law
Reasoning: Clause establishes which jurisdiction's law will govern the agreement.

Clause: "Either party may terminate this Agreement with 30 days' notice."
Label: Termination
Reasoning: Clause describes conditions under which contract ends.

Clause: "Each party agrees to keep all information confidential."
Label: Confidentiality
Reasoning: Clause binds parties to maintain secrecy of information.

Clause: "Party A shall indemnify Party B against any losses incurred."
Label: Indemnity
Reasoning: Clause allocates responsibility for loss or damage between parties.

"""

LABEL_SET = ["Governing Law", "Termination", "Confidentiality", "Indemnity", "Jurisdiction", "Payment", "Obligations", "Other"]

def classify_clause_llm(clause_text, url=LMSTUDIO_URL, model=MODEL_NAME, labels=LABEL_SET):
    prompt = f"""{FEW_SHOT_EXAMPLES}

Clause: "{clause_text}"
Label and Reasoning: (format as Label: <label>\nReasoning: <explanation>)
"""
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "max_tokens": 200,
    }
    response = requests.post(url, json=body)
    if not response.ok:
        raise RuntimeError(f"LLM API error: {response.status_code} {response.text}")
    raw = response.json()["choices"][0]["message"]["content"].strip()
    # Split and parse output
    label, reasoning = ("Other", "No reasoning returned.")
    for l in labels:
        if raw.lower().startswith(f"label: {l.lower()}"):
            label = l
            break
        if f"label: {l.lower()}" in raw.lower():
            label = l
            break
    # Try to extract reasoning
    for line in raw.split("\n"):
        if line.lower().startswith("reasoning:"):
            reasoning = line.split(":",1)[1].strip()
    return {"label": label, "reasoning": reasoning, "raw": raw}
