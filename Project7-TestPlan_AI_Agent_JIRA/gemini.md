# 📜 Project Constitution (gemini.md)

## 1. Data Schemas
**[DRAFT]** Derived from `promt.md` for the Intelligent Test Plan Agent. Must be approved.

### Input Shape (Jira Issue Payload)
```json
{
  "issue_id": "string",
  "title": "string",
  "description": "string",
  "acceptance_criteria": "string",
  "issue_type": "string",
  "priority": "string",
  "labels": ["string"],
  "attachments": [{"filename": "string", "url": "string"}],
  "comments": [{"author": "string", "body": "string"}]
}
```

### Output Shape (Generated Test Plan Payload)
```json
{
  "test_objectives": "string",
  "scope": "string",
  "functional_test_scenarios": ["string"],
  "non_functional_test_scenarios": ["string"],
  "api_test_scenarios": ["string"],
  "risk_analysis": "string",
  "test_data_requirements": "string",
  "entry_criteria": "string",
  "exit_criteria": "string"
}
```

## 2. Behavioral Rules
- **Security:** Encrypt API keys and securely store passwords.
- **Validation:** Always validate Jira Input (Issue ID) before sending requests.
- **Integrity:** Rate limit LLM requests to prevent service interruptions.
- **Delivery:** Must be able to export results securely to PDF/DOCX.

## 3. Architectural Invariants
- **Layer 1 (Architecture):** Technical SOPs in Markdown.
- **Layer 2 (Navigation):** Reasoning and routing layer.
- **Layer 3 (Tools):** Deterministic Python/Node/React logic (Backend/Frontend).
- No coding in `tools/` until the Blueprint is approved.
- Use `.tmp/` for all intermediate file operations.
