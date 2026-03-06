Objective

Build a full-stack web application called "Intelligent Test Plan Agent" that automatically generates a structured software test plan from a Jira issue using an LLM (Cloud or Local via Ollama) and a predefined test plan template.

Core Features
1. User Authentication

The application should support basic authentication.

Features:

User registration

User login/logout

Secure password storage

Session management

2. Settings Page

The Settings page allows users to configure integrations.

Jira Configuration

Users must provide:

Jira Base URL

Jira Email

Jira API Token

Store these securely.

Provide a "Test Connection" button to verify the Jira connection.

LLM Configuration

The user should be able to choose between:

Option 1: Cloud LLM

Provider (OpenAI / Groq / etc.)

API Key

Model name

Option 2: Local LLM

Ollama URL (default: http://localhost:11434)

Model name (example: llama3, mistral)

Add a Test Model Connection button.

3. Jira Issue Input

Provide a simple UI where the user can enter:

Jira Issue ID
Example:

PROJ-101

Buttons:

Fetch Issue
Generate Test Plan

4. Fetch Jira Details

When the user clicks Fetch Issue, the application should retrieve:

Issue Title

Description

Acceptance Criteria

Issue Type

Priority

Labels

Attachments

Comments

Display the fetched information in the UI.

5. Test Plan Template

The system will use a test plan template stored in the server.

Folder:

/templates/test_plan_template.pdf

The template contains sections such as:

Test Plan Identifier

Introduction

Scope

Test Strategy

Test Environment

Test Scenarios

Test Cases

Risks and Mitigation

Entry Criteria

Exit Criteria

Deliverables

Schedule

The application must read this structure and send it to the LLM.

6. Test Plan Generation Using LLM

When the user clicks Generate Test Plan, the system should:

Fetch Jira issue data.

Load the test plan template structure.

Combine both into a structured prompt.

Send the prompt to the selected LLM (Cloud or Ollama).

Generate a detailed test plan.

The generated test plan should include:

Test Objectives

Scope

Functional Test Scenarios

Non-Functional Test Scenarios

API Test Scenarios (if applicable)

Risk Analysis

Test Data Requirements

Entry and Exit Criteria

7. Output Generation

The generated test plan should be exportable as:

PDF

DOCX

Users should be able to:

Download
Edit before download

8. Dashboard

The dashboard should show:

Recently generated test plans

Jira issue used

Date created

Download option

9. Application UI Pages

Create the following pages:

Login Page

Register Page

Dashboard

Settings

Test Plan Generator Page

Test Plan Preview Page

10. Suggested Tech Stack

Frontend

React.js or Next.js
Tailwind CSS

Backend

Python FastAPI or Node.js Express

Database

PostgreSQL or SQLite

LLM Integration

LangChain or direct API calls

Jira Integration

Jira REST API

Local LLM

Ollama API

11. Project Folder Structure

Example structure:

intelligent-test-plan-agent
│
├── backend
│   ├── api
│   ├── services
│   ├── jira_service.py
│   ├── llm_service.py
│   ├── template_service.py
│
├── frontend
│   ├── pages
│   ├── components
│
├── templates
│   └── test_plan_template.pdf
│
├── database
│
└── README.md
12. Security Considerations

Encrypt API keys

Secure authentication

Validate Jira input

Rate limit LLM requests

Expected Result

A working web application where a user can:

Connect Jira

Configure an LLM (Cloud or Ollama)

Enter a Jira Issue ID

Fetch issue details

Automatically generate a complete professional test plan

Export the test plan as PDF or DOCX