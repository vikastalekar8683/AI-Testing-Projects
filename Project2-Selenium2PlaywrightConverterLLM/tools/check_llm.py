import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "codellama")

def check_ollama_connection():
    try:
        print(f"Testing connection to Ollama at {BASE_URL}...")
        
        # 1. Check if Ollama is running
        resp = requests.get(f"{BASE_URL}/")
        if resp.status_code == 200:
            print("[OK] Ollama server is running.")
        else:
            print(f"[ERROR] Ollama server reachable but returned status: {resp.status_code}")
            return False

        # 2. Check if Model exists
        print(f"Checking for model: {MODEL}...")
        resp = requests.get(f"{BASE_URL}/api/tags")
        if resp.status_code == 200:
            models = resp.json().get("models", [])
            model_names = [m["name"] for m in models]
            
            # Allow for tag variations (e.g. codellama:latest)
            found = any(MODEL in name for name in model_names)
            
            if found:
                print(f"[OK] Model '{MODEL}' found locally.")
                return True
            else:
                print(f"[WARN] Model '{MODEL}' NOT found. Available models: {model_names}")
                print("Tip: Run `ollama pull codellama`")
                return False
        else:
            print(f"[ERROR] Failed to list models. Status: {resp.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Could not connect to {BASE_URL}. Is Ollama running?")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

if __name__ == "__main__":
    check_ollama_connection()
