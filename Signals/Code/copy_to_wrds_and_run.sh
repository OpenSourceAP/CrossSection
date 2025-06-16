#!/bin/bash

# run this from Signals/Code/
# philosphy is: two distinct projects:
# 1. Signals/Code/
# 2. Portfolios/Code/

# Load credentials (check paths)
source .env

# Define local and remote directories
LOCAL_DIR="$(pwd)"
REMOTE_DIR="~/PrepScripts"

echo "Copying PrepScripts to WRDS server..."

# Copy entire PrepScripts directory to WRDS server
sshpass -p "$WRDS_PASSWORD" scp -o StrictHostKeyChecking=no -r "$LOCAL_DIR" "$WRDS_USERNAME@wrds-cloud.wharton.upenn.edu:~/"

echo "Submitting master.sh job to WRDS queue with email notifications..."

# Connect to WRDS server and submit master.sh as a job with email notification
JOB_OUTPUT=$(sshpass -p "$WRDS_PASSWORD" ssh -o StrictHostKeyChecking=no "$WRDS_USERNAME@wrds-cloud.wharton.upenn.edu" "cd $REMOTE_DIR && chmod +x master.sh && qsub -m e -M ayc1678@gmail.com master.sh")
echo "Job submitted: $JOB_OUTPUT"

# Extract job ID from output (format: "Your job 123456 ("master.sh") has been submitted")
JOB_ID=$(echo "$JOB_OUTPUT" | grep -o '[0-9]\+' | head -n1)

if [ -n "$JOB_ID" ]; then
    echo "Job ID: $JOB_ID"
    echo "Streaming job output log (press Ctrl+C to stop)..."
    echo "Note: Log may take a few seconds to appear as job starts..."
    
    # Stream the job output log
    sshpass -p "$WRDS_PASSWORD" ssh -o StrictHostKeyChecking=no "$WRDS_USERNAME@wrds-cloud.wharton.upenn.edu" "cd $REMOTE_DIR && tail -f master.sh.o$JOB_ID 2>/dev/null || (echo 'Waiting for log file to be created...' && sleep 5 && tail -f master.sh.o$JOB_ID)"
else
    echo "Could not extract job ID. Job may have failed to submit."
fi