from interfaces.llm_client import LLMClient
from core.config import Config
import re

class InferenceService:
    def __init__(self):
        self.client = LLMClient()
        self.few_shot_examples = """
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

    def analyze_clause(self, clause_text):
        prompt = f"""{self.few_shot_examples}

Clause: "{clause_text}"
Label and Reasoning: (format as Label: <label>\nReasoning: <explanation>)
"""
        raw = self.client.generate(prompt)
        
        label, reasoning = ("Other", "No reasoning returned.")
        for l in Config.LABEL_SET:
            if raw.lower().startswith(f"label: {l.lower()}"):
                label = l
                break
            if f"label: {l.lower()}" in raw.lower():
                label = l
                break
        
        # Try to extract reasoning
        for line in raw.split("\n"):
            if line.lower().startswith("reasoning:"):
                reasoning = line.split(":", 1)[1].strip()
        
        return {
            "label": label, 
            "reasoning": reasoning,
            "text": clause_text
        }
