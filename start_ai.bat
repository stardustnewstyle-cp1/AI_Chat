@echo off
cd /d %~dp0

REM 仮想環境
call "%~dp0..\venv\Scripts\activate.bat"

REM Frontend 起動
cd /d "%~dp0frontend"
start "Frontend" cmd /k python -m http.server 8080

timeout /t 2 >nul
start "" http://localhost:8080

REM FastAPI 起動
cd /d "%~dp0"
start "FastAPI" cmd /k python -m uvicorn backend.api.main:app --reload

pause