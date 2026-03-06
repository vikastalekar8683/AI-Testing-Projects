import os
import requests
import json
from requests.auth import HTTPBasicAuth

def fetch_jira_issue(issue_id):
    """
    SOP: Layer 3 Tool -> Fetches a specific Jira issue and returns a normalized payload.
    """
    jira_url = os.environ.get('JIRA_BASE_URL', '').rstrip('/')
    email = os.environ.get('JIRA_EMAIL')
    api_token = os.environ.get('JIRA_API_TOKEN')

    if not jira_url or not email or not api_token:
        raise ValueError("Missing Jira Configuration in Environment variables.")

    url = f"{jira_url}/rest/api/3/issue/{issue_id}"
    auth = HTTPBasicAuth(email, api_token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)
    
    if response.status_code == 401:
        raise PermissionError("Jira Authentication failed. Check API Token and Email.")
    if response.status_code == 404:
        raise FileNotFoundError(f"Jira issue '{issue_id}' not found.")
    
    response.raise_for_status()
    data = response.json()

    # Save intermediate payload mapping to .tmp for debugging
    tmp_path = os.path.join('.tmp', f"{issue_id}_raw.json")
    os.makedirs('.tmp', exist_ok=True)
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    fields = data.get('fields', {})
    
    # Parse Description (Jira Atlassian Document Format)
    desc_str = ""
    description_obj = fields.get('description')
    if description_obj and isinstance(description_obj, dict):
        # Extract text from the complex Atlassian Document Format
        for content_block in description_obj.get('content', []):
            for paragraph_content in content_block.get('content', []):
                desc_str += paragraph_content.get('text', '') + "\n"
    elif isinstance(description_obj, str):
        desc_str = description_obj

    payload = {
        "issue_id": issue_id,
        "title": fields.get("summary", ""),
        "description": desc_str.strip(),
        "issue_type": fields.get("issuetype", {}).get("name", "Unknown"),
        "priority": fields.get("priority", {}).get("name", "Unknown"),
        "labels": fields.get("labels", [])
    }
    
    return payload

def test_jira_connection():
    jira_url = os.environ.get('JIRA_BASE_URL', '').rstrip('/')
    email = os.environ.get('JIRA_EMAIL')
    api_token = os.environ.get('JIRA_API_TOKEN')

    if not jira_url or not email or not api_token:
        raise ValueError("Missing Jira Configuration in Environment variables.")

    url = f"{jira_url}/rest/api/3/myself"
    auth = HTTPBasicAuth(email, api_token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)
    
    if response.status_code == 200:
        data = response.json()
        return f"Connected as: {data.get('displayName')} ({data.get('emailAddress')})"
    elif response.status_code == 401:
        raise PermissionError("Jira Authentication failed. Check API Token and Email.")
    else:
        raise ConnectionError(f"Jira connection failed. Status code: {response.status_code}")

if __name__ == "__main__":
    # Test block
    from dotenv import load_dotenv
    load_dotenv()
    print(json.dumps(fetch_jira_issue("PROJ-101"), indent=2))
