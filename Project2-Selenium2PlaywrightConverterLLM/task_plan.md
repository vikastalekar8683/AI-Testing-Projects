# Task Plan

## Goals
Develop a web-based "Selenium to Playwright" converter that uses an LLM to transform Java/TestNG code into TypeScript/Playwright code. The system requires a User Interface for input/output and a robust backend conversion engine.

## Phases

### Phase 1: Blueprint (Vision & Logic)
- [x] Define Discovery Requirements
- [x] Define Data Schemas in `gemini.md`
- [ ] Research: Map common Selenium patterns to Playwright (Wait strategies, Locators).

### Phase 2: Link (Connectivity)
- [ ] Set up LLM Connection (Ollama/OpenAI) via `tools/check_llm.py`.
- [ ] Create `.env` for configuration.

### Phase 3: Architect (The 3-Layer Build)
- [ ] Create `architecture/conversion_sop.md`: Define the prompt engineering strategy.
- [ ] Create `tools/llm_client.py`: Wrapper for LLM interactions.
- [ ] Create `tools/converter.py`: Core conversion logic.

### Phase 4: Stylize (Refinement & UI)
- [ ] Build Backend API (Flask/FastAPI) to expose `tools/converter.py`.
- [ ] Build Frontend (HTML/CSS/JS) for code input and result display.
- [ ] Implement side-by-side diff view.

### Phase 5: Trigger (Deployment)
- [ ] Finalize "One-Click Run" script.
- [ ] Documentation.

## Checklists
### Urgent
- [ ] Verify Local LLM (Ollama) availability.

