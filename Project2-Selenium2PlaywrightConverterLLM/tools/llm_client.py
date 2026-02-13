import requests
import json
import os
from typing import Dict, Any

class LLMClient:
    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "codellama")
    
    def generate(self, prompt: str, system_prompt: str = "", stream: bool = False):
        """
        Sends a prompt to the Ollama API and returns the response.
        If stream=True, returns a generator yielding response chunks.
        """
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": stream,
            "options": {
                "temperature": 0.1,  # Low temp for deterministic code
                "num_ctx": 4096      # Larger context for code files
            }
        }
        
        try:
            response = requests.post(url, json=payload, stream=stream)
            response.raise_for_status()
            
            if stream:
                def generate_chunks():
                    for line in response.iter_lines():
                        if line:
                            try:
                                json_response = json.loads(line)
                                chunk = json_response.get("response", "")
                                if chunk:
                                    yield chunk
                                if json_response.get("done", False):
                                    break
                            except json.JSONDecodeError:
                                pass
                return generate_chunks()
            else:
                return response.json().get("response", "")
                
        except requests.exceptions.RequestException as e:
            msg = f"Error communicating with LLM: {str(e)}"
            return iter([msg]) if stream else msg

# Singleton instance for easy import
client = LLMClient()
