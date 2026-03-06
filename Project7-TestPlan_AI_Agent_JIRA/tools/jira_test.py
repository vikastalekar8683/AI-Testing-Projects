import os
import requests
from requests.auth import HTTPBasicAuth

def load_env():
    env_vars = {}
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    return env_vars

def main():
    env_vars = load_env()
    jira_url = env_vars.get('JIRA_BASE_URL')
    email = env_vars.get('JIRA_EMAIL')
    api_token = env_vars.get('JIRA_API_TOKEN')

    print(f"Testing Jira connection to: {jira_url}")

    auth = HTTPBasicAuth(email, api_token)
    headers = {
        "Accept": "application/json"
    }

    # Ping the myself endpoint to verify auth
    url = f"{jira_url.rstrip('/')}/rest/api/3/myself"
    
    try:
        response = requests.get(url, headers=headers, auth=auth)

        if response.status_code == 200:
            print("[SUCCESS] Jira Connection Successful!")
            data = response.json()
            print(f"Authenticated as: {data.get('displayName')} ({data.get('emailAddress')})")
        else:
            print(f"[FAILED] Jira Connection Failed! Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] Exception occurred while connecting to Jira: {str(e)}")

if __name__ == "__main__":
    main()
