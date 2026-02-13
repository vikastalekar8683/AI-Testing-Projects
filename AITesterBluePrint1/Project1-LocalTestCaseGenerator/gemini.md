# Project Constitution: Local LLM Testcase Generator (gemini.md)

## Data Schemas
### Ollama Request
```json
{
  "model": "qwen3:4b",
  "prompt": "string",
  "stream": true
}
```

### Chat State
```json
{
  "messages": [
    { "role": "user", "content": "source_code" },
    { "role": "assistant", "content": "generated_tests" }
  ],
  "isThinking": "boolean"
}
```

## Behavioral Rules
- **UI Interaction**: User enters code -> App wraps code in a test-generation template -> Ollama generates -> Assistant displays.
- **Formatting**: Always wrap output in Markdown code blocks.
- **Error Handling**: Gracefully handle Ollama connection failures with a "Connection Error" UI state.

## Architectural Invariants
- **Layer 1 (API)**: `src/api/ollama.js` (Handles fetches)
- **Layer 2 (Logic)**: `src/logic/promptEngine.js` (Handles templates)
- **Layer 3 (UI)**: `src/ui/chat.js` (Handles chat rendering)
