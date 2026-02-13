@echo off
setlocal
cd /d %~dp0

REM venvが存在しない場合のみ作成する
if not exist "venv" (
    echo 仮想環境を作成中...
    python -m venv venv
)

echo 実行開始...
.\venv\Scripts\python.exe pochiNaviEmp.py

pause