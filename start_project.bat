@echo off
title Blockchain Voting System Launcher
echo ========================================================
echo  Launching Blockchain Voting System (Backend + Frontend)
echo ========================================================
echo.

:: 1. Launch FastAPI Backend in a new window
echo [1/2] Launching Backend API Server (FastAPI on Port 8000)...
start "Backend API Server (FastAPI)" cmd /k ".\backend\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

:: 2. Launch React Vite Frontend in a new window
echo [2/2] Launching Frontend Web App (React + Vite on Port 5173)...
start "Frontend Web App (React)" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================================
echo  Success! Both servers are running in parallel.
echo  - Backend Docs: http://127.0.0.1:8000/docs
echo  - Frontend App:  http://localhost:5173
echo ========================================================
echo.
