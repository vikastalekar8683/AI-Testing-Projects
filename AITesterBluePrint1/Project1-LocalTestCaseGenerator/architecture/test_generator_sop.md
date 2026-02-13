# SOP: Test Case Generation Logic

## 1. Goal
Generate comprehensive, deterministic test cases for provided source code snippets using the local Ollama `qwen3:4b` model.

## 2. Inputs
- `source_code`: The code snippet provided by the user.
- `model_name`: Defaulting to `qwen3:4b`.
- `prompt_template`: The specific instructions wrapping the source code.

## 3. Tool Logic (Layer 3: Python)
1. **Tool**: `tools/ollama_tool.py`
2. **Action**: Communicates with local Ollama via `httpx`.
3. **Behavior**: Provides a streaming generator for the LLM response.

## 4. Navigation (Layer 2: Python Backend)
1. **Gateway**: `backend/main.py` (FastAPI).
2. **Routing**: Receives UI requests, calls the Python tools, and streams response back to the browser.

## 4. Edge Cases & Constraints
- **Ollama Offline**: Trigger "Connection Error" alert.
- **Malformed Response**: Fallback to raw text if JSON parsing fails.
- **Large Code**: Model context window limits (warn user if exceeded).

## 5. Decision Routing (Navigation)
- If input is empty -> UI Prompt for more info.
- If Ollama is ready -> Execute generation.
- If generator fails -> Log to findings.md and notify user.
