
import httpx
import json
import os

OLLAMA_BASE_URL = "http://localhost:11434"

async def generate_completion(model: str, prompt: str):
    """
    Deterministic Python tool to communicate with Ollama.
    """
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True
    }
    
    async with httpx.AsyncClient(timeout=None) as client:
        try:
            async with client.stream("POST", url, json=payload) as response:
                if response.status_code != 200:
                    print(f"Ollama Error: {response.status_code}")
                    yield f"Error: Ollama returned {response.status_code}"
                    return
                
                print(f"Started streaming from Ollama model: {model}")
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        chunk = data.get("response", "")
                        if chunk:
                            yield chunk
                        if data.get("done"):
                            print("Streaming Complete.")
                            break
        except Exception as e:
            print(f"Tool Error: {str(e)}")
            yield f"Error: {str(e)}"

if __name__ == "__main__":
    # Test script
    import asyncio
    async def test():
        async for chunk in generate_completion("qwen3:4b", "Say hello"):
            print(chunk, end="", flush=True)
    asyncio.run(test())
