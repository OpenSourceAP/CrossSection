#!/bin/bash

## ABOUTME: downloads prep data from WRDS server to local pyData/Prep/ folder
## ABOUTME: run after prep_on_wrds.sh. Run this from Signals/pyCode/

# Load credentials (check paths)
# .env should look like this:
# WRDS_USERNAME=your_username
# WRDS_PASSWORD=your_password

if [ ! -f .env ]; then
    echo "Error: .env file not found in $(pwd)"
    echo "Please create .env file with WRDS_USERNAME and WRDS_PASSWORD"
    exit 1
fi

source .env # should be in Signals/pyCode/

# Define local and remote directories
LOCAL_DIR="../pyData/Prep"
REMOTE_DIR="~/temp_prep/data_for_dl"

echo "Here are the contents of the remote directory: ($REMOTE_DIR)"
sshpass -p "$WRDS_PASSWORD" ssh -o StrictHostKeyChecking=no "$WRDS_USERNAME@wrds-cloud.wharton.upenn.edu" "ls -la $REMOTE_DIR/"

# check with user about proceeding
echo ""
echo "Here are the contents of the local directory: ($LOCAL_DIR)"
ls -la "$LOCAL_DIR/"

read -p "Proceed with downloading? (y/n): " proceed
if [ "$proceed" != "y" ]; then
    echo "Quitting."
    exit 0
fi

# download files
sshpass -p "$WRDS_PASSWORD" scp -o StrictHostKeyChecking=no "$WRDS_USERNAME@wrds-cloud.wharton.upenn.edu:$REMOTE_DIR/*.csv" "$LOCAL_DIR/"