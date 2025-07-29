@echo off
REM PDF Stitcher Batch Script for Windows
REM This script makes it easy to run the PDF stitcher without typing the full Python command

echo PDF Stitcher - Quick Launch
echo ============================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import pypdf, click" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install required packages
        pause
        exit /b 1
    )
)

REM Run the PDF stitcher with all passed arguments
python pdf_stitcher.py %*

REM Pause if run by double-clicking (not from command line)
if "%1"=="" pause
