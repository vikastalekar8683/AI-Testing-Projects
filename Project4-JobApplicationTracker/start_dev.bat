@echo off
start "Backend Server" cmd /k "cd backend && .venv\Scripts\activate && uvicorn main:app --reload || pause"
start "Frontend Server" cmd /k "cd frontend && npm run dev || pause"
echo Job Application Tracker started!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
