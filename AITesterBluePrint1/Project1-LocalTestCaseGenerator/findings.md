# Findings: Local LLM Testcase Generator

## Research & Discoveries
- **Protocol**: B.L.A.S.T.
- **North Star**: Local LLM testcase generator using Ollama (qwen3:4b) with a templated prompt.
- **Integration**: Ollama API (`http://localhost:11434`)
- **Delivery Payload**: A UI Chat interface for code input and test generation.
- **Models**: `qwen3:4b` (Primary), `gemma3:4b` (Legacy Support)
- **OS**: Windows

## Constraints
- Local execution only.
- Must follow A.N.T. 3-layer architecture.
- Behavior: Input -> Ollama Processing -> Test Case Output.
