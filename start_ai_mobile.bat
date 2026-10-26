@echo off
cd /d %~dp0

echo ==========================================
echo   技術質問AIアシスタント（スマホ版）
echo   起動準備中...
echo ==========================================

REM --- payload.zip を展開 ---
if not exist payload.zip (
    echo payload.zip が見つかりません。BAT と同じ場所に置いてください。
    pause
    exit /b
)

echo ZIP を展開しています...
powershell -command "Expand-Archive -Path 'payload.zip' -DestinationPath 'app' -Force"

cd app

REM --- 仮想環境を起動 ---
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo 仮想環境が見つかりません。payload.zip が壊れている可能性があります。
    pause
    exit /b
)

REM --- PC の IP アドレス取得 ---
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do set IP=%%a
set IP=%IP: =%

echo 使用するIPアドレス: %IP%

REM --- バックエンド起動（LAN 公開） ---
start "" uvicorn backend.api.main:app --host 0.0.0.0 --port 8000

REM --- フロントエンド起動（LAN 公開） ---
cd frontend
start "" python -m http.server 8080 --bind 0.0.0.0

echo.
echo ==========================================
echo   スマホで以下を開いてください：
echo.
echo       http://%IP%:8080
echo.
echo   ※同じWi-Fiに接続している必要があります
echo ==========================================
echo.
pause
