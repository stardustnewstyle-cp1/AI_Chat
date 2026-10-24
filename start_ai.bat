@echo off
cd /d %~dp0

call venv\Scripts\activate.bat

REM ブラウザを開く
start "" http://localhost:8080

REM フロントを起動
cd frontend
start "" python -m http.server 8080

REM FastAPI を起動
cd ..
uvicorn backend.api.main:app --reload