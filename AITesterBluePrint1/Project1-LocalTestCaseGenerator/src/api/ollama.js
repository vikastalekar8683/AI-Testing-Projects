const BACKEND_URL = 'http://127.0.0.1:8000/api/generate';

export async function generateTestCases(model, prompt, onChunk) {
    try {
        const response = await fetch(BACKEND_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: model,
                prompt: prompt
            })
        });

        if (!response.ok) throw new Error('Ollama connection failed');

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const textChunk = decoder.decode(value, { stream: true });
            fullResponse += textChunk;
            onChunk(textChunk, fullResponse);
        }
        return fullResponse;
    } catch (error) {
        console.error('Inference Error:', error);
        throw error;
    }
}

export async function checkOllamaStatus() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/health');
        return response.ok;
    } catch {
        return false;
    }
}
