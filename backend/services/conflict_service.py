from interfaces.llm_client import LLMClient
from itertools import combinations

class ConflictService:
    def __init__(self):
        self.client = LLMClient()

    def detect_rule_based(self, chunks):
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
        return results

    def detect_llm(self, clause_pairs):
        results = []
        for c1, c2 in clause_pairs:
            prompt = f"""Do these two contract clauses contradict each other or create ambiguity?
Clause 1: {c1}
Clause 2: {c2}
Answer in this format:
Conflicted: [Yes|No]
ConflictType: <type or none>
Explanation: <short explanation>
"""
            try:
                answer = self.client.generate(prompt, temperature=0.0, max_tokens=300)
                if 'conflicted:yes' in answer.lower():
                    lines = answer.split('\n')
                    typ, expl = 'Unknown', 'No further details.'
                    for ln in lines:
                        if ln.lower().startswith('conflicttype:'):
                            typ = ln.split(':', 1)[1].strip()
                        if ln.lower().startswith('explanation:'):
                            expl = ln.split(':', 1)[1].strip()
                    results.append({
                        "conflict_type": typ,
                        "clauses": [c1, c2],
                        "detection": "LLM",
                        "explanation": expl
                    })
            except:
                continue
        return results

    def get_clause_pairs(self, chunks, max_len=100):
        filtered = [c for c in chunks if len(c) > 30]
        pairs = list(combinations(filtered, 2))
        return pairs[:max_len]
