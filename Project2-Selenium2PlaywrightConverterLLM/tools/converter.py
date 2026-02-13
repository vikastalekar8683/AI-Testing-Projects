import sys
import os
import re
from pathlib import Path
 # Add project root to path if not already added
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.llm_client import client

def convert_selenium_to_playwright_stream(source_code: str):
    """
    Orchestrates the conversion of Selenium Java code to Playwright TypeScript using streaming.
    Yields chunks of generated code.
    """
    
    system_prompt = """You are an expert SDET and Code Transpiler.
    Your task is to convert Selenium Java (TestNG) code to equivalent Playwright TypeScript code.
    
    RULES:
    1. Output strictly TypeScript code.
    2. Use 'test', 'expect' from '@playwright/test'.
    3. Convert @Test to test(), @BeforeMethod to test.beforeEach().
    4. Convert By.id/css/xpath to page.locator().
    5. Convert driver.findElement().click() to await page.click() or await page.locator().click().
    6. Ensure all interactions are awaited.
    7. Do NOT wrap output in markdown code blocks (```). Return RAW code only.
    8. If a line is ambiguous, add a comment: // TODO: Manual review needed.
    """
    
    prompt = f"""
    Convert the following Java Selenium code to Playwright TypeScript:
    
    {source_code}
    
    Output ONLY raw code. Do NOT use markdown code blocks.
    """
    
    print("ðŸ”„ Sending code to LLM for available stream...")
    return client.generate(prompt=prompt, system_prompt=system_prompt, stream=True)

if __name__ == "__main__":
    # Test stub
    sample_java = """
    @Test
    public void loginTest() {
        driver.get("https://example.com");
    }
    """
    for chunk in convert_selenium_to_playwright_stream(sample_java):
        print(chunk, end="", flush=True)
