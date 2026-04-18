from interfaces.llm_client import LLMClient
import json

class SummarizerService:
    def __init__(self):
        self.client = LLMClient()
        self.schema = """
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

    def summarize(self, contract_text, clause_infos):
        context = "\n".join([f"Clause: {ci['text']}\nType: {ci['label']}\nRisk: {ci.get('risk','')}\nReasoning: {ci.get('reasoning','')}" for ci in clause_infos])
        prompt = f"{self.schema}\nContract begins:\n{contract_text[:4000]}\n\nKey extracted clauses and risk info:\n{context}\n"
        
        raw = self.client.generate(prompt, max_tokens=2000)
        
        try:
            first_brace = raw.find('{')
            last_brace = raw.rfind('}')
            if first_brace != -1 and last_brace != -1:
                raw_json = raw[first_brace:last_brace+1]
                return json.loads(raw_json)
            return {"error": "JSON not found in LLM response", "raw": raw}
        except Exception as e:
            return {"error": f"Failed to parse JSON: {str(e)}", "raw": raw}
