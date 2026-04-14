import requests
import os
from itertools import combinations

LMSTUDIO_URL = os.getenv("LMSTUDIO_URL", "http://127.0.0.1:1234/v1/chat/completions")
MODEL_NAME = os.getenv("LMSTUDIO_MODEL", "mistral")

def detect_conflicts_rule_based(chunks):
    """
    Detects simple pattern-based contradictions in a list of text chunks.
    Returns list of {conflict_type, clauses, detection, explanation}
    """
    results = []
    lower_chunks = [c.lower() for c in chunks]
    # Example: Exclusivity contradiction
    found_exc = [i for i, c in enumerate(lower_chunks) if "exclusive right" in c]
    found_nonexc = [i for i, c in enumerate(lower_chunks) if "non-exclusive right" in c]
    if found_exc and found_nonexc:
        results.append({
            "conflict_type": "Exclusivity Contradiction",
            "clauses": [chunks[found_exc[0]], chunks[found_nonexc[0]]],
            "detection": "Rule-based",
            "explanation": "Contract uses both 'exclusive' and 'non-exclusive' rights."
        })
    # Add more rule-based patterns as needed (date conflicts, IP ownership, etc)
    return results

def detect_conflicts_llm(clause_pairs, url=LMSTUDIO_URL, model=MODEL_NAME):
    """
    Input: list of (clause1, clause2)
    Output: list of detected LLM-based conflicts, each as dict
    """
    results = []
    for c1, c2 in clause_pairs:
        prompt = f"""Do these two contract clauses contradict each other or create ambiguity?\nClause 1: {c1}\nClause 2: {c2}\nAnswer in this format:\nConflicted:[Yes|No]\nConflictType:<type or none>\nExplanation:<short explanation>\n"""
        body = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
            "max_tokens": 300,
        }
        resp = requests.post(url, json=body)
        if not resp.ok:
            continue
        answer = resp.json()["choices"][0]["message"]["content"].strip()
        if 'conflicted:yes' in answer.lower():
            # parse out type and explanation:
            lines = answer.split('\n')
            typ, expl = 'Unknown', 'No further details.'
            for ln in lines:
                if ln.lower().startswith('conflicttype:'):
                    typ = ln.split(':',1)[1].strip()
                if ln.lower().startswith('explanation:'):
                    expl = ln.split(':',1)[1].strip()
            results.append({
                "conflict_type": typ,
                "clauses": [c1, c2],
                "detection": "LLM",
                "explanation": expl
            })
    return results

def all_clause_pairs(chunks, max_len=300):
    """
    Utility: returns pairs of (chunk1, chunk2) for comparison, skips obviously short/irrelevant.
    """
    filtered = [c for c in chunks if len(c) > 30]
    pairs = list(combinations(filtered, 2))
    return pairs[:max_len]  # safety limit
