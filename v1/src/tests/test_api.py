import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

@patch('src.services.inference_service.InferenceService.client.generate')
def test_analyze_risk(mock_generate):
    mock_generate.return_value = "Type: Indemnity\nRisk: High\nExplanation: This is high risk."
    response = client.post("/api/v1/analyze-risk", json={"clause": "The vendor shall indemnify."})
    assert response.status_code == 200
    data = response.json()
    assert "clause" in data
    assert "type" in data
    assert "risk" in data
    assert "explanation" in data
    assert "confidence" in data
    assert data["risk"] == "High"

@patch('src.services.inference_service.InferenceService.client.generate')
def test_ask(mock_generate):
    mock_generate.return_value = "The answer is yes."
    response = client.post("/api/v1/ask", json={"question": "What is the termination clause?", "context": "Either party may terminate with notice."})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data

@patch('src.services.inference_service.InferenceService.client.generate')
def test_summarize(mock_generate):
    mock_generate.return_value = "This is a summary."
    response = client.post("/api/v1/summarize", json={"text": "This is a contract."})
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data