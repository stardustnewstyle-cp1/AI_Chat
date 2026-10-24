@echo off
REM ================================
REM  Tech AI Assistant 起動スクリプト
REM  hide 専用（Copilot風 UI）
REM ================================

REM プロジェクトのルートへ移動
cd /d C:\Users\Owner\source\AIchat\pipeline

REM 仮想環境を起動
call venv\Scripts\activate

REM フロントエンド（Copilot風 UI）をブラウザで開く
start "" "C:\Users\Owner\source\AIchat\pipeline\frontend\index.html"

REM FastAPI バックエンドを起動
uvicorn backend.api.main:app --reload
