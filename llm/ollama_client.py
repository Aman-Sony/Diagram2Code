# llm/ollama_client.py

import requests
import json

def generate_code_with_ollama(prompt: str, model: str = "qwen") -> str:
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            return f"❌ Error: Ollama returned status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"❌ Ollama request failed: {str(e)}"
