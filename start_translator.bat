@echo off
title Advanced Subtitle Translator
echo 🚀 Starting Advanced Subtitle Translator...
echo 📱 Loading application...

REM Try to run with Python
python start_translator.py

REM If python command not found, try py
if %ERRORLEVEL% neq 0 (
    echo 💡 Trying alternative Python command...
    py start_translator.py
)

REM If still failed, try python3
if %ERRORLEVEL% neq 0 (
    echo 💡 Trying python3 command...
    python3 start_translator.py
)

REM If all failed, show error
if %ERRORLEVEL% neq 0 (
    echo ❌ Error: Python not found or script failed
    echo 💡 Please make sure Python is installed and in PATH
    echo 💡 Or run manually: python start_translator.py
    pause
)
