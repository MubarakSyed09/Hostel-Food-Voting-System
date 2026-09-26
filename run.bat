@echo off
title Hostel Mess Smart Food Voting System
echo ========================================================
echo Starting Hostel Mess Smart Food Voting System...
echo Pure Python GUI Application (Baby Blue Edition)
echo ========================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python main.py
) else (
    "C:\Users\megha\AppData\Local\Programs\Python\Python312\python.exe" main.py
)

pause
