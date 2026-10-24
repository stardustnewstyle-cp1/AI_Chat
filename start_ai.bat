@echo off
cd /d %~dp0

REM 古い uvicorn と python を落とす
taskkill /F /IM python.exe 2>nul
taskkill /F /IM uvicorn.exe 2>nul

call venv\Scripts\activate.bat

REM フロントを起動
cd frontend
start "" python -m http.server 8080

REM 少し待つ
timeout /t 2 >nul

REM ブラウザを開く
start "" http://localhost:8080

REM FastAPI を起動
cd ..
uvicorn backend.api.main:app --reload