from src.services.inference_service import InferenceService

# Mock the generate method for testing
class MockClient:
    def generate(self, prompt):
        if "Analyze the clause" in prompt:
            return "Type: Indemnity\nRisk: High\nExplanation: This clause imposes high risk."
        elif "Generate a concise explanation" in prompt:
            return "This clause is high risk because it requires indemnification."
        else:
            return "Mock response"

service = InferenceService()
service.client = MockClient()

# Test analyze_clause
result = service.analyze_clause("The vendor shall indemnify the customer.")
print("Test result:", result)
assert result["type"] == "Indemnity"
assert result["risk"] == "High"
print("Inference service test passed.")