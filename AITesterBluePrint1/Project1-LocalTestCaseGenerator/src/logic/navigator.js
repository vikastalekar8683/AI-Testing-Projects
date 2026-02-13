
/**
 * Layer 2: Navigation (Decision Making)
 * Routes data between Architecture SOPs and Layer 3 Tools.
 */
import { buildPrompt } from './promptEngine.js';
import { generateTestCases } from '../api/ollama.js';

export async function executeTestGeneration(sourceCode, onUpdate) {
    console.log("🚀 Navigator: Initiating test generation workflow...");

    // 1. Logic Layer (SOP Compliance)
    try {
        const fullPrompt = buildPrompt(sourceCode);

        // 2. Execution Layer (Tool Calling)
        const model = "qwen3:4b";
        await generateTestCases(model, fullPrompt, (chunk, full) => {
            onUpdate(full);
        });

        console.log("✅ Navigator: Workflow complete.");
    } catch (error) {
        console.error("❌ Navigator Error:", error.message);
        throw error;
    }
}
