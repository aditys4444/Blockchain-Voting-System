Write-Host "========================================================" -ForegroundColor Cyan
Write-Host " Launching Blockchain Voting System (Backend + Frontend)" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

$rootPath = $PSScriptRoot

Write-Host "[1/2] Launching Backend API Server (FastAPI on Port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootPath'; .\backend\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

Write-Host "[2/2] Launching Frontend Web App (React on Port 5173)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootPath\frontend'; npm run dev"

Write-Host ""
Write-Host "========================================================" -ForegroundColor Green
Write-Host " Success! Both servers are running in parallel." -ForegroundColor Green
Write-Host " - Backend API:  http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host " - Frontend App: http://localhost:5173" -ForegroundColor White
Write-Host "========================================================" -ForegroundColor Green
