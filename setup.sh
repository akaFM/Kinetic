#!/usr/bin/env sh

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

if ! command_exists python3; then
    echo "Error: Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

if ! command_exists pip; then
    echo "Error: pip is not installed. Please install pip and try again."
    exit 1
fi

echo "Setting up the virtual environment..."
python3 -m venv env || { echo "Error: Failed to create the virtual environment."; exit 1; }

echo "Activating the virtual environment..."
source env/bin/activate || { echo "Error: Failed to activate the virtual environment."; exit 1; }

echo "Installing dependencies..."
pip install -r requirements.txt || { echo "Error: Failed to install dependencies."; exit 1; }