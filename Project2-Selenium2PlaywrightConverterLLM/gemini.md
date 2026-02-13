# Project Constitution

## Data Schemas

### 1. Conversion Request (Input)
```json
{
  "source_code": "String (Raw Java Selenium Code)",
  "source_framework": "String (Default: 'TestNG')",
  "target_language": "String (Enum: 'JavaScript', 'TypeScript')",
  "model_preference": "String (Optional, e.g., 'gpt-4', 'llama3')"
}
```

### 2. Conversion Response (Output)
```json
{
  "status": "String ('success', 'error')",
  "converted_code": "String (Playwright Code)",
  "explanation": "String (Markdown explanation of changes)",
  "file_path": "String (Path to saved file, if applicable)",
  "error_message": "String (Null if success)"
}
```

## Behavioral Rules
1. **Total Conversion:** Attempt to convert 100% of the logic, including explicit waits, locators, and assertions.
2. **Framework Mapping:** Map TestNG annotations (`@Test`, `@BeforeMethod`, etc.) to Playwright equivalents (`test()`, `test.beforeEach()`).
3. **Safety First:** If a construct cannot be converted (e.g., specific Java library dependency), add a comment in the code explaining why.
4. **Deterministic Output:** Ensure the generated code is syntactically correct and formatted.

## Architectural Invariants
1. **Separation of Concerns:** The Core Conversion Logic (Python Tool) must be decoupled from the UI (Frontend).
2. **Stateless Core:** The conversion tool should accept input, process, and return output without retaining session state.
3. **Local-First:** Prioritize local execution (Local LLM/Ollama) but allow for API overrides.

## Maintenance Log
<!-- Log for long-term stability -->
