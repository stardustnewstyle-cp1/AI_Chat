@echo off
cd /d %~dp0

REM 既存の uvicorn プロセスだけを停止
taskkill /F /IM uvicorn.exe 2>nul

call venv\Scripts\activate.bat

cd frontend
start "" python -m http.server 8080

timeout /t 2 >nul
start "" http://localhost:8080

cd ..
uvicorn backend.api.main:app --reload