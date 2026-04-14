import requests
import json

URL = "http://127.0.0.1:8000/summarize"
payload = {
    "contract_text": "This is a sample contract. Party A agrees to pay Party B $100. Termination is on notice of 30 days."
}

try:
    print(f"Sending request to {URL}...")
    response = requests.post(URL, json=payload)
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(json.dumps(response.json(), indent=2))
    
    if "summary" in response.json():
        print("\nSUCCESS: 'summary' key found.")
    else:
        print("\nFAILURE: 'summary' key MISSING.")
except Exception as e:
    print(f"Error connecting to backend: {e}")
