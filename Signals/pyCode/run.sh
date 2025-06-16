#!/bin/bash

# Activate virtual environment and run master.py
# This is the main entry point for the pyCode project

set -e  # Exit on any error

# Check if we're in the right directory
if [ ! -f "CLAUDE.md" ]; then
    echo "Error: Please run this script from the pyCode directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found. Please run set_up_pyCode.py first"
    exit 1
fi

# Activate virtual environment and run master.py
echo "Activating virtual environment and running master.py..."
source .venv/bin/activate
python master.py