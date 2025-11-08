@echo off
REM Script to install dependencies and run the text transformer application on Windows

echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% == 0 (
    echo Dependencies installed successfully!
    echo Starting Text Transformer Application...
    echo Press Ctrl+C to exit
    python text_transformer.py
) else (
    echo Failed to install dependencies. Please check your internet connection and try again.
    pause
    exit /b 1
)