# 📘 LLM Generator SOP

## 1. Goal
Take the structured Jira Input Data Payload and securely feed it into the selected LLM (Cloud or Local/Ollama) alongside a pre-defined instruction prompt based on the test plan template, yielding the structured Output Schema payload.

## 2. Inputs
- `jira_payload`: JSON string/dict representing the normalized Jira issue.
- `llm_type`: "local" or "cloud".
- `model_name`: e.g., "gpt-oss:120b", "openai", "groq".
- `OLLAMA_URL`: Default `http://localhost:11434`.
- `API_KEY`: Only if `llm_type` is cloud.

## 3. Tool Logic
1. Verify the selected `llm_type`.
2. Format the Master Prompt:
    - Inject the "System Prompt" instructing the LLM to act as a QA Engineer.
    - Append the `jira_payload` data.
    - Define the strictly required Output Schema format (JSON) from `gemini.md`.
3. If `llm_type` == "local":
    - Make a POST request to `{OLLAMA_URL}/api/generate`.
    - Provide `{"model": model_name, "prompt": prompt, "stream": False, "format": "json"}`.
4. If `llm_type` == "cloud":
    - Make the respective API call to OpenAI or Groq, requesting a JSON object back.
5. Extract the generated `response_text`.
6. Validate that the text is strictly parseable as JSON.
7. Return the validated Test Plan Data Object to Layer 2 (Navigation).

## 4. Edge Cases & Handling
- **Ollama Offline (Connection refused):** If the request to `http://localhost:11434` fails, catch the `ConnectionError` and return an explicit UI message instructing the user to start the Ollama service.
- **Malformed JSON:** Probabilistic LLMs sometimes include markdown `` ```json `` fences in the output. The tool must strip these out before running `json.loads()`.
- **Timeouts:** Complex test plans require high output tokens. Set aggressive but realistic timeout thresholds (e.g., 60-120 seconds).
