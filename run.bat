@echo off
title MapLead Outscraper Setup and Runner
echo ===================================================
echo   MapLead Outscraper Automated Startup
echo ===================================================

:: Check if the user is running the script from inside a ZIP file (without extracting)
echo "%~dp0" | findstr /i "AppData\Local\Temp" >nul
if %ERRORLEVEL% == 0 (
    echo [ERROR] You are running this script inside the ZIP file!
    echo.
    echo Please EXTRACT the ZIP folder first to a normal folder 
    echo (e.g., your Desktop), and then run run.bat from there.
    echo.
    pause
    exit /b
)

cd /d "%~dp0outscraper-python"

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not installed on your system!
    echo.
    echo Please install Python to run this project. 
    echo Opening the official Python download page in your browser...
    echo.
    echo IMPORTANT: During installation, make sure to check the box:
    echo            "[x] Add python.exe to PATH"
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b
)

:: Check if the virtual environment folder exists
if not exist "venv\Scripts\activate.bat" (
    echo ===================================================
    echo  [SETUP] Creating Python Virtual Environment (venv)...
    echo ===================================================
    python -m venv venv || (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b
    )
    
    echo ===================================================
    echo  [SETUP] Installing dependencies (this may take a minute)...
    echo ===================================================
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt || (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b
    )

    echo ===================================================
    echo  [SETUP] Installing Playwright Web Browser...
    echo ===================================================
    playwright install chromium || (
        echo [ERROR] Failed to install Playwright browser.
        pause
        exit /b
    )
    echo ===================================================
    echo  [SETUP] Setup completed successfully!
    echo ===================================================
    echo.
)

:: Activate the virtual environment
call venv\Scripts\activate.bat

:: Start a background process to wait 3 seconds and open the browser
echo Opening http://127.0.0.1:8000 in your browser...
start /b cmd /c "ping -n 4 127.0.0.1 >nul && (start chrome http://127.0.0.1:8000 || start http://127.0.0.1:8000)"

:: Start FastAPI server using uvicorn
python -m uvicorn app:app --reload

pause
