#!/usr/bin/env sh

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

if command_exists python3; then
    PYTHON_CMD="python3"
elif command_exists python && [ "$(python --version 2>&1 | awk '{print $2}' | cut -d. -f1)" -ge 3 ]; then
    PYTHON_CMD="python"
else
    echo "Error: Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

if command_exists pip3; then
    PIP_CMD="pip3"
elif command_exists pip; then
    PIP_CMD="pip"
else
    echo "Error: pip is not installed. Please install pip and try again."
    exit 1
fi

echo "Setting up the virtual environment..."
"$PYTHON_CMD" -m venv .venv || { echo "Error: Failed to create the virtual environment."; exit 1; }

echo "Activating the virtual environment..."
. .venv/bin/activate || { echo "Error: Failed to activate the virtual environment."; exit 1; }

echo "Installing dependencies..."
"$PIP_CMD" install -r requirements.txt || { echo "Error: Failed to install dependencies."; exit 1; }

echo "Virtual environment created in '.venv'."
echo "To activate it, run:"
echo ""
echo "source .venv/bin/activate"
echo ""