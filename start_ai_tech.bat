@echo off
cd /d %~dp0

REM --- 仮想環境を起動 ---
call venv\Scripts\activate

REM --- バックエンド起動 ---
start "" uvicorn backend.api.main:app --host 0.0.0.0 --port 8000

REM --- フロントエンド起動（ローカル HTTP） ---
cd frontend
start "" python -m http.server 8080

echo ==========================================
echo  技術質問AIアシスタント（PC版）
echo  http://localhost:8080 を開いてください
echo ==========================================
pause
