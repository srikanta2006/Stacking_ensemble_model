@echo off
REM Quick Start Script for KC House Price Prediction

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║  KC House Price Prediction - Stacking Ensemble          ║
echo ║  Quick Start Guide                                       ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org
    pause
    exit /b 1
)

echo ✅ Python found!
echo.

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not available
    pause
    exit /b 1
)

echo ✅ pip found!
echo.

REM Install requirements
echo 📦 Installing required packages...
echo    (This may take a few minutes on first run)
echo.
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ❌ Failed to install packages
    echo Please check your internet connection
    pause
    exit /b 1
)

echo.
echo ✅ All packages installed successfully!
echo.

REM Run Streamlit app
echo 🚀 Starting Streamlit application...
echo.
echo    Opening in browser at: http://localhost:8501
echo.
echo 📌 To stop the app, press CTRL+C in this window
echo.
echo ════════════════════════════════════════════════════════════
echo.

streamlit run streamlit_app.py

pause
