
/**
 * Layer 3: Atomic Prompt Construction Tool
 */
export const PILOT_TEMPLATE = `
Act as an expert software tester. Analyze the code provided below and generate a comprehensive set of test cases.
Follow this format:
1. **Test Scenario**: What is being tested.
2. **Setup**: Necessary prerequisites.
3. **Execution Steps**: Step-by-step instructions.
4. **Expected Results**: Correct behavior.
Include positive, negative, and edge-case scenarios.

CODE TO TEST:
{CODE}
`;

export function buildPrompt(sourceCode) {
    if (!sourceCode || sourceCode.trim() === "") {
        throw new Error("Source code is required for test generation.");
    }
    return PILOT_TEMPLATE.replace("{CODE}", sourceCode);
}
