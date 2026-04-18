import requests
import os

from core.config import Config

class LLMClient:
    def __init__(self, url=None, model=None):
        self.url = url or Config.LMSTUDIO_URL
        self.model = model or Config.LMSTUDIO_MODEL

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
