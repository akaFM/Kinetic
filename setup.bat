@echo off
setlocal

:: Check for Python3
python --version | findstr "Python 3" > nul
if errorlevel 1 (
    python3 --version | findstr "Python 3" > nul
    if errorlevel 1 (
        echo Error: Python 3 is not installed. Please install Python 3 and try again.
        exit /b 1
    ) else (
        set PYTHON_CMD=python3
    )
) else (
    set PYTHON_CMD=python
)

:: Check for pip
%PYTHON_CMD% -m pip --version > nul
if errorlevel 1 (
    echo Error: pip is not installed. Please install pip and try again.
    exit /b 1
)

echo Setting up the virtual environment...
%PYTHON_CMD% -m venv .venv
if errorlevel 1 (
    echo Error: Failed to create the virtual environment.
    exit /b 1
)

echo Activating the virtual environment...
call .venv\Scripts\activate
if errorlevel 1 (
    echo Error: Failed to activate the virtual environment.
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies.
    exit /b 1
)

echo Virtual environment created in '.venv'.
echo To activate it, run:
echo.
echo .venv\Scripts\activate
echo. 