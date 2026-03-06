import os
import requests
import json

def generate_test_plan(jira_payload, llm_type="local", model_name="gpt-oss:120b"):
    """
    SOP: Layer 3 Tool -> Connects to AI model and transforms Jira issue into JSON test plan output.
    """
    
    # 1. Define a focused System Prompt to request deep detail and structured cases
    system_prompt = f"""Task: Act as an expert QA Automation Engineer. Generate a HIGHLY DETAILED Software Test Plan for the Jira issue provided below.

JIRA ISSUE PAYLOAD:
{json.dumps(jira_payload, indent=2)}

INSTRUCTIONS:
1. CRITICAL: Your output MUST be valid JSON.
2. TEST OBJECTIVES: List specific goals for this feature (Array of strings).
3. SCOPE: List what is IN and what is OUT of scope (Array of strings).
4. TEST CASES: Create detailed objects. Steps MUST be an array of strings.
5. NON-FUNCTIONAL: List performance, security, and usability points (Array of strings).
6. FORMATTING: For multi-line text sections (like objectives or risks), ALWAYS use an ARRAY OF STRINGS. 

JSON SCHEMA (FOLLOW EXACTLY):
{{
  "test_objectives": ["string"],
  "scope": ["string"],
  "detailed_test_cases": [
    {{
      "id": "TC-01",
      "title": "string",
      "preconditions": "string",
      "steps": ["Step 1", "Step 2"],
      "expected_result": "string",
      "priority": "High/Medium/Low"
    }}
  ],
  "non_functional_scenarios": ["string"],
  "api_test_scenarios": ["string"],
  "risk_analysis": ["string"],
  "test_data_requirements": ["string"],
  "entry_criteria": ["string"],
  "exit_criteria": ["string"]
}}
"""

    if llm_type == "local":
        ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
        url = f"{ollama_url}/api/generate"
        payload = {
            "model": model_name,
            "prompt": system_prompt,
            "stream": False,
            "format": "json"
        }
        
        try:
            # Increased timeout to 300 seconds (5 minutes) for heavy local models
            response = requests.post(url, json=payload, timeout=300)
            response.raise_for_status()
            data = response.json()
            raw_output = data.get("response", "{}")
            
            # Save raw output to tmp for debugging
            os.makedirs('.tmp', exist_ok=True)
            with open(os.path.join('.tmp', 'llm_raw_output.json'), 'w', encoding='utf-8') as f:
                f.write(raw_output)
                
            # Attempt to parse as strict json
            test_plan = json.loads(raw_output)
            return test_plan
            
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Ollama took too long to respond (>300s). Try a smaller model or check system resources.")
        except requests.exceptions.ConnectionError:
            raise ConnectionError(f"Cannot connect to Ollama at {ollama_url}. Is Ollama running?")
        except json.JSONDecodeError:
            raise ValueError(f"LLM returned invalid JSON. Raw output: {raw_output[:100]}...")
            
    elif llm_type == "cloud":
        # Determine Cloud Provider from model_name or context
        # Typical pattern: "openai:gpt-4o" or "groq:llama3-8b-8192"
        provider = "openai"
        actual_model = model_name
        
        if ":" in model_name:
            provider, actual_model = model_name.split(":", 1)
        
        try:
            if provider.lower() == "openai":
                api_key = os.environ.get("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("Missing 'OPENAI_API_KEY' in .env file. Please add it or switch to a Groq model in Settings.")
                
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model=actual_model,
                    messages=[{"role": "user", "content": system_prompt}],
                    response_format={ "type": "json_object" }
                )
                raw_output = response.choices[0].message.content
                
            elif provider.lower() == "groq":
                api_key = os.environ.get("GROQ_API_KEY")
                if not api_key:
                    raise ValueError("Missing 'GROQ_API_KEY' in .env file. Please add it or switch to a different model.")

                from groq import Groq
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model=actual_model,
                    messages=[{"role": "user", "content": system_prompt}],
                    response_format={ "type": "json_object" }
                )
                raw_output = response.choices[0].message.content

            elif provider.lower() == "google":
                api_key = os.environ.get("GEMINI_API_KEY")
                if not api_key:
                    raise ValueError("Missing 'GEMINI_API_KEY' in .env file. Get one for free at: aistudio.google.com")

                import google.generativeai as genai
                genai.configure(api_key=api_key)
                # Configuration for structured JSON
                generation_config = {
                  "temperature": 1,
                  "top_p": 0.95,
                  "top_k": 40,
                  "max_output_tokens": 8192,
                  "response_mime_type": "application/json",
                }
                
                model = genai.GenerativeModel(
                  model_name=actual_model,
                  generation_config=generation_config,
                )
                
                chat_session = model.start_chat()
                response = chat_session.send_message(system_prompt)
                raw_output = response.text
            else:
                raise ValueError(f"Unsupported cloud provider: {provider}")

            # Save raw output to tmp for debugging
            os.makedirs('.tmp', exist_ok=True)
            with open(os.path.join('.tmp', 'llm_cloud_raw_output.json'), 'w', encoding='utf-8') as f:
                f.write(raw_output)

            test_plan = json.loads(raw_output)
            return test_plan

        except Exception as e:
            raise RuntimeError(f"Cloud LLM Error ({provider}): {str(e)}")
    else:
        raise ValueError("Invalid LLM Type selected.")

if __name__ == "__main__":
    # Test stub
    dummy_payload = {
      "issue_id": "TEST-1",
      "title": "Add User Login Endpoint",
      "description": "Create a secure user login REST API using JWT tokens.",
      "issue_type": "Story",
      "priority": "High"
    }
    print("Testing generator (Requires Ollama)...")
    # print(json.dumps(generate_test_plan(dummy_payload, "local", "Mistral"), indent=2))
