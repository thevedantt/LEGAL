import requests
import os

class LLMClient:
    def __init__(self, url=None, model=None):
        self.url = url or os.getenv("LMSTUDIO_URL", "http://127.0.0.1:1234/v1/chat/completions")
        self.model = model or os.getenv("LMSTUDIO_MODEL", "mistral")

    def generate(self, prompt, temperature=0.2, max_tokens=400):
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise RuntimeError(f"Error connecting to LLM: {str(e)}")
