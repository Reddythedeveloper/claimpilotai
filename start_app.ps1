$ErrorActionPreference = "Stop"

Write-Host "Starting ClaimPilot AI services..." -ForegroundColor Cyan

# Start FastAPI Backend
Write-Host "Starting FastAPI Backend on port 8000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\venv\Scripts\Activate.ps1; uvicorn app.main:app --reload"

# Start Next.js Frontend
Write-Host "Starting Next.js Frontend on port 3000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "Services started! You can close this window." -ForegroundColor Green
