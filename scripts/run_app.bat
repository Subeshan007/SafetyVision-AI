@echo off
echo ========================================
echo  SafetyVision AI - Launch Script
echo ========================================
echo.
echo Starting application...
echo.

python safety_vision_app.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo ERROR: Failed to start application
    echo ========================================
    echo.
    echo Possible issues:
    echo 1. Python not found in PATH
    echo 2. Required packages not installed
    echo 3. Model file not found
    echo.
    echo Try running: pip install tkinter pillow opencv-python
    echo.
    pause
)
