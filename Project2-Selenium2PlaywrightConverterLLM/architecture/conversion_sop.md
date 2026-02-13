# SOP: LLM Conversion Strategy

## Goal
Reliably convert Selenium (Java) code to Playwright (TS/JS) using a local LLM.

## Prompt Engineering Strategy

### 1. Role Definition
The LLM must act as a **Senior SDET** (Software Development Engineer in Test) combined with a **Compiler**. It should not be "chatty".

### 2. Context Injection
We must provide the LLM with:
- The **Rules** (from `gemini.md`)
- The **Source Code**
- A **Target Template** (optional, but ensures consistent structure)

### 3. Step-by-Step Prompt Structure
1.  **System Instruction**: "You are a code transpiler. Input: Java Selenium. Output: Playwright TypeScript. Strict syntax."
2.  **Constraint List**:
    - "Use `page.locator()` instead of `driver.findElement`."
    - "Convert `@Test` to `test('name', async ({ page }) => { ... })`."
    - "Convert `Assert.assertEquals` to `expect(val).toBe(expected)`."
3.  **Input**: The raw Java code.
4.  **Output Indicator**: "```typescript"

## Error Handling
If the LLM hallucinates or fails:
1.  **Retry**: Increase temperature slightly? (Unlikely for code).
2.  **Fallback**: Return the raw completion but flag it as "Review Needed".

## Model Specifics (CodeLlama)
CodeLlama is good at syntax but may struggle with complex architectural shifts. We must break down large files if they exceed context, but for MVP we assume files < 4000 tokens.
