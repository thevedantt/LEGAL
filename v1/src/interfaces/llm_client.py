import requests


class LLMClient:
    def __init__(self, url="http://localhost:1234/v1/chat/completions"):
        self.url = url

    def generate(self, prompt, model="mistral-7b-instruct-v0.2"):
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 400
        }
        
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error connecting to LLM: {str(e)}"
