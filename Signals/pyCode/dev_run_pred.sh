#!/bin/bash

# send_iMessage function
send_iMessage() {
  local TO="$1" MSG="$2"
  /usr/bin/osascript <<EOF
tell application "Messages"
  set theService to 1st service whose service type = iMessage
  set theBuddy to buddy "$TO" of theService
  send "$MSG" to theBuddy
end tell
EOF
}

# Start notification
echo "Starting predictor creation and validation..."
send_iMessage "+12404465313" "🚀 Started: Predictor creation and validation pipeline"

# Run 02_CreatePredictors.py
echo "Running 02_CreatePredictors.py..."
if python3 02_CreatePredictors.py; then
    send_iMessage "+12404465313" "✅ Step 1 Complete: 02_CreatePredictors.py finished successfully"
    echo "02_CreatePredictors.py completed successfully"
    
    # Run test_predictors.py --all
    echo "Running utils/test_predictors.py --all..."
    if python3 utils/test_predictors.py --all; then
        send_iMessage "+12404465313" "🎉 All Complete: Both predictor creation and validation finished successfully"
        echo "All tasks completed successfully"
    else
        send_iMessage "+12404465313" "❌ Step 2 Failed: test_predictors.py validation failed"
        echo "test_predictors.py failed"
        exit 1
    fi
else
    send_iMessage "+12404465313" "❌ Step 1 Failed: 02_CreatePredictors.py failed"
    echo "02_CreatePredictors.py failed"
    exit 1
fi

echo "Script completed. Check your messages for notifications."