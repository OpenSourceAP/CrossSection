#!/bin/bash

# run this from Signals/Code/
# philosphy is: two distinct projects:
# 1. Signals/Code/
# 2. Portfolios/Code/

# Load credentials (check paths)
# .env should look like this:
# WRDS_USERNAME=your_username
# WRDS_PASSWORD=your_password

if [ ! -f .env ]; then
    echo "Error: .env file not found in $(pwd)"
    echo "Please create .env file with WRDS_USERNAME and WRDS_PASSWORD"
    exit 1
fi

source .env # should be in Signals/Code/

# Define local and remote directories
LOCAL_DIR="PrepScripts"
REMOTE_DIR="~/temp_prep"

echo "Copying PrepScripts to WRDS server ~/temp_prep"

# Create remote directory structure first
sshpass -p "$WRDS_PASSWORD" ssh -o StrictHostKeyChecking=no "$WRDS_USERNAME@wrds-cloud.wharton.upenn.edu" "mkdir -p $REMOTE_DIR"

# Copy PrepScripts directory contents to WRDS server
sshpass -p "$WRDS_PASSWORD" scp -o StrictHostKeyChecking=no -r "$LOCAL_DIR"/* "$WRDS_USERNAME@wrds-cloud.wharton.upenn.edu:$REMOTE_DIR/"

# Prompt for email notification
echo "Submitting job to WRDS queue."
read -p "Enter email for job notifications (press enter to skip, 'q' to quit): " EMAIL

# Connect to WRDS server and submit master.sh as a job with email notification if provided
if [ "$EMAIL" == "q" ]; then
    echo "Quitting."
    exit 0
elif [ -z "$EMAIL" ]; then
    JOB_OUTPUT=$(sshpass -p "$WRDS_PASSWORD" ssh -o StrictHostKeyChecking=no "$WRDS_USERNAME@wrds-cloud.wharton.upenn.edu" "cd $REMOTE_DIR && chmod +x run_all_prep.sh && qsub run_all_prep.sh")
else
    JOB_OUTPUT=$(sshpass -p "$WRDS_PASSWORD" ssh -o StrictHostKeyChecking=no "$WRDS_USERNAME@wrds-cloud.wharton.upenn.edu" "cd $REMOTE_DIR && chmod +x run_all_prep.sh && qsub -m e -M $EMAIL run_all_prep.sh")
fi

echo "Job submitted: $JOB_OUTPUT"

# run qstat once
sshpass -p "$WRDS_PASSWORD" ssh -o StrictHostKeyChecking=no "$WRDS_USERNAME@wrds-cloud.wharton.upenn.edu" "qstat"

echo "Impatient? Check most recent file in ~/temp_prep/log/ on WRDS server."
