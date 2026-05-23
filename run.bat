@echo off
title MapLead Outscraper Server
echo ===================================================
echo   Starting MapLead Outscraper Server...
echo ===================================================

cd /d "%~dp0outscraper-python"

if not exist venv\Scripts\activate.bat (
    echo [ERROR] Python virtual environment not found.
    pause
    exit /b
)

call venv\Scripts\activate.bat

echo Opening http://127.0.0.1:8000 in browser...
start /b cmd /c "ping -n 3 127.0.0.1 >nul && (start chrome http://127.0.0.1:8000 || start http://127.0.0.1:8000)"

python -m uvicorn app:app --reload

pause
