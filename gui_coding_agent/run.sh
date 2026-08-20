#!/usr/bin/env bash
# run.sh - Simple wrapper to set up and run the terminal GUI coding agent

set -e

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if not already installed
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the agent
echo "Running the coding agent..."
python run.py