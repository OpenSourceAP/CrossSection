#!/bin/bash

# Activate virtual environment and run master.py
# This is the main entry point for the pyCode project

set -e  # Exit on any error

# Function to print timestamped messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}


# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found. Please run set_up_pyCode.py first"
    exit 1
fi

# Start execution
log_message "🚀 Starting pyCode execution pipeline"
log_message "📁 Working directory: $(pwd)"

# Activate virtual environment and run master.py
log_message "🐍 Activating virtual environment..."
source .venv/bin/activate

log_message "▶️  Starting master.py execution"
python -u master.py

log_message "✅ Pipeline execution completed successfully"