from src.interfaces.llm_client import LLMClient
import re


class InferenceService:
    def __init__(self):
        self.client = LLMClient()

    def build_prompt(self, clause):
        examples = """
Example 1:
Clause: The vendor shall indemnify and hold harmless the customer from any claims arising from the vendor's negligence.
Type: Indemnity
Risk: High
Explanation: This clause requires the vendor to cover all losses due to their negligence, posing high financial risk.

Example 2:
Clause: Either party may terminate this agreement with 30 days written notice.
Type: Termination
Risk: Medium
Explanation: Allows termination with notice, which is standard but could disrupt operations.

Example 3:
Clause: All information shared shall remain confidential.
Type: Confidentiality
Risk: Low
Explanation: Standard confidentiality clause with minimal risk if properly defined.
"""
        return f"""
You are a legal contract analysis assistant.

Analyze the clause below and return ONLY in this format:
Type: [Clause Type]
Risk: [Low/Medium/High]
Explanation: [Brief explanation]

{examples}

Clause: {clause}

Output:
"""

    def extract_output(self, response):
        type_match = re.search(r'Type:\s*(.+)', response, re.IGNORECASE)
        risk_match = re.search(r'Risk:\s*(Low|Medium|High)', response, re.IGNORECASE)
        explanation_match = re.search(r'Explanation:\s*(.+)', response, re.IGNORECASE)
        
        clause_type = type_match.group(1).strip() if type_match else "Unknown"
        risk = risk_match.group(1).strip() if risk_match else "Medium"
        explanation = explanation_match.group(1).strip() if explanation_match else "No explanation provided"
        
        return clause_type, risk

    def final_risk(self, clause, predicted_type, llm_risk):
        rules = {
            "Liability": "High",
            "Indemnity": "High",
            "Termination": "Medium",
            "Confidentiality": "Low"
        }
        if predicted_type in rules:
            return rules[predicted_type]
        return llm_risk

    def generate_explanation(self, clause, clause_type, risk):
        prompt = f"""
Generate a concise explanation for why this clause is classified as {risk} risk.

Clause: {clause}
Type: {clause_type}
Risk: {risk}

Explanation:
"""
        return self.client.generate(prompt)

    def compute_confidence(self, clause, clause_type, risk, rule_applied):
        # Heuristic: 0.9 if rule applied, else 0.7
        if rule_applied:
            return 0.9
        # Check for keywords
        high_keywords = ["liability", "indemnify", "unlimited"]
        if any(kw in clause.lower() for kw in high_keywords) and risk == "High":
            return 0.8
        return 0.7

    def analyze_clause(self, clause):
        prompt = self.build_prompt(clause)
        response = self.client.generate(prompt)
        predicted_type, llm_risk = self.extract_output(response)
        final_risk = self.final_risk(clause, predicted_type, llm_risk)
        rule_applied = predicted_type in ["Liability", "Indemnity", "Termination", "Confidentiality"] and final_risk != llm_risk
        explanation = self.generate_explanation(clause, predicted_type, final_risk)
        confidence = self.compute_confidence(clause, predicted_type, final_risk, rule_applied)
        
        return {
            "clause": clause,
            "type": predicted_type,
            "risk": final_risk,
            "explanation": explanation,
            "confidence": confidence
        }



