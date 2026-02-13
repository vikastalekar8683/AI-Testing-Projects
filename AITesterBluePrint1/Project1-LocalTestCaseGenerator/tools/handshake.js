
async function testOllama() {
    console.log("🚀 Initializing Handshake with Ollama...");
    try {
        const response = await fetch('http://localhost:11434/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: "qwen3:4b",
                prompt: "Say 'Ollama is Ready' if you are alive.",
                stream: false
            })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();
        console.log("✅ Handshake Successful!");
        console.log("Response:", data.response);
    } catch (error) {
        console.error("❌ Handshake Failed!");
        console.error("Error:", error.message);
        process.exit(1);
    }
}

testOllama();
