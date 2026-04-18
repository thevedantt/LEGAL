from core.config import Config
from interfaces.llm_client import LLMClient
import re

class RiskAnalyzer:
    def __init__(self):
        self.client = LLMClient()

    def rule_based_risk_flags(self, text):
        flags = []
        low_text = text.lower()
        if "indemnify" in low_text or "hold harmless" in low_text:
            flags.append("Indemnity")
        if "unlimited liability" in low_text or "shall be liable for all" in low_text:
            flags.append("Unlimited Liability")
        if "automatic renewal" in low_text or "forever" in low_text:
            flags.append("Duration/Renewal")
        return flags

    def llm_risk_score(self, text):
        prompt = f"""Rate the legal risk of this contract clause on a scale of 1 to 10.
1 = Very Low Risk, 10 = Critical Risk.
Return your answer as "Score: <num>\nReasoning: <explanation>".

Clause: "{text}"
"""
        response = self.client.generate(prompt)
        
        score_match = re.search(r"Score:\s*(\d+)", response)
        reason_match = re.search(r"Reasoning:\s*(.+)", response, re.DOTALL)
        
        score = score_match.group(1) if score_match else "5"
        reason = reason_match.group(1).strip() if reason_match else "No reasoning provided."
        
        return score, reason
