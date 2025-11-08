@echo off
REM Setup script for V-USB Driver Installer
REM This script prepares the Windows driver installer

setlocal enabledelayedexpansion

echo.
echo ========================================
echo V-USB Driver Installer Setup
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✓ Python found
python --version

echo.
echo Installing dependencies...
pip install -r requirements_windows_installer.txt

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ✓ Dependencies installed successfully

echo.
echo Building Windows executable...
python build_windows_installer.py

if %errorlevel% neq 0 (
    echo Error: Failed to build executable
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Executable location: dist\V-USB Driver Installer.exe
echo.
echo Next steps:
echo 1. Run the executable as Administrator
echo 2. Connect your Arduino device
echo 3. Click "Detect Device"
echo 4. Click "Install Driver"
echo.
pause
