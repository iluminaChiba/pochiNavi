@echo off
echo pochiNavi実行中...
echo.

REM === スクリプトのあるフォルダに移動 ===
cd /d "%~dp0"
echo 作業ディレクトリ: %CD%

REM === Pythonの確認 ===
python --version >nul 2>&1
if errorlevel 1 (
    echo エラー: Pythonが見つかりません
    echo Pythonがインストールされているか確認してください
    pause
    exit /b 1
)

REM === 必要ファイルの確認 ===
if not exist "pochiNavi.py" (
    echo エラー: pochiNavi.pyが見つかりません
    pause
    exit /b 1
)

if not exist "config.json" (
    echo エラー: config.jsonが見つかりません
    pause
    exit /b 1
)

REM === Pythonを使ってスクリプトを実行 ===
echo Pythonスクリプトを実行中...
python pochiNavi.py

REM === 終了コードの確認 ===
if errorlevel 1 (
    echo.
    echo スクリプトの実行中にエラーが発生しました (終了コード: %errorlevel%)
) else (
    echo.
    echo スクリプトが正常に完了しました
)

REM === 実行後にキー入力を待つ ===
echo.
pause
