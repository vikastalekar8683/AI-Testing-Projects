# 📘 Jira Fetcher SOP

## 1. Goal
To securely fetch complete issue details from the Jira REST API using a given `Issue ID` and format the response according to the precise Input Schema defined in `gemini.md`.

## 2. Inputs
- `issue_id`: The project tag and ticket number (e.g., "PROJ-101").
- `JIRA_BASE_URL`: Loaded from `.env`
- `JIRA_EMAIL`: Loaded from `.env`
- `JIRA_API_TOKEN`: Loaded from `.env`

## 3. Tool Logic
1. Validate the `issue_id` format (must contain a hyphen and numbers).
2. Construct the API Endpoint: `{JIRA_BASE_URL}/rest/api/3/issue/{issue_id}`.
3. Apply `requests.auth.HTTPBasicAuth`.
4. Send a `GET` request to Jira.
5. Parse the JSON response.
6. Extract the exact fields mapped in the Input Data Schema (`title`, `description`, `acceptance_criteria`, `issue_type`, `priority`, `labels`, `attachments`, `comments`).
7. Save the raw response temporarily in `.tmp/jira_raw_response.json` (for debugging).
8. Return the normalized dictionary/JSON payload to Layer 2 (Navigation).

## 4. Edge Cases & Handling
- **401 Unauthorized:** The credentials in `.env` are invalid. Return early with a clear error block.
- **404 Not Found:** The `issue_id` does not exist. Alert the user in the UI.
- **Missing Fields:** Some tickets might not have `acceptance_criteria` or `attachments`. The dictionary parser must use `.get()` with safe defaults (e.g., `""` or `[]`) to prevent KeyError crashes.
