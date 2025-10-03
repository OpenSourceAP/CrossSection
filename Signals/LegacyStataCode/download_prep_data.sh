#!/bin/bash

# Download prep data from WRDS server to local Data/Prep/ folder
# Run this from Signals/Code/ directory
# Data is created by prep_on_wrds.sh and stored in ~/temp_prep/data_for_dl/ on WRDS

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
LOCAL_PREP_DIR="../Data/Prep"
REMOTE_DATA_DIR="~/temp_prep/data_for_dl"

echo "Downloading prep data from WRDS server to local Data/Prep/ folder"

# Create local Data/Prep directory if it doesn't exist
mkdir -p "$LOCAL_PREP_DIR"

# List of prep data files created by run_all_prep.sh:
# - iclink.csv (IBES-CRSP link)
# - oclink.csv (OptionMetrics-CRSP link)
# - tr_13f.csv (13F institutional holdings)
# - corwin_schultz_spread.csv (low-frequency spreads)
# - hf_monthly.csv (high-frequency spreads from Chen-Velikov)
# - OptionMetricsVolSurf.csv (option metrics volatility surface)
# - OptionMetricsVolume.csv (option metrics volume data)
# - OptionMetricsXZZ.csv (additional option metrics data)
# - bali_hovak_imp_vol.csv (Bali-Hovak implied volatility)

echo "Files to be downloaded:"
echo "- iclink.csv (IBES-CRSP link)"
echo "- oclink.csv (OptionMetrics-CRSP link)"
echo "- tr_13f.csv (13F institutional holdings)"
echo "- corwin_schultz_spread.csv (low-frequency spreads)"
echo "- hf_monthly.csv (high-frequency spreads)"
echo "- OptionMetricsVolSurf.csv (option metrics volatility surface)"
echo "- OptionMetricsVolume.csv (option metrics volume data)"
echo "- OptionMetricsXZZ.csv (additional option metrics data)"
echo "- bali_hovak_imp_vol.csv (Bali-Hovak implied volatility)"

# Check what files are available on WRDS server
echo ""
echo "Checking available files on WRDS server..."
sshpass -p "$WRDS_PASSWORD" ssh -o StrictHostKeyChecking=no "$WRDS_USERNAME@wrds-cloud.wharton.upenn.edu" "ls -la $REMOTE_DATA_DIR/"

echo ""
echo "Downloading files..."

# Download all CSV files from the remote data directory
sshpass -p "$WRDS_PASSWORD" scp -o StrictHostKeyChecking=no "$WRDS_USERNAME@wrds-cloud.wharton.upenn.edu:$REMOTE_DATA_DIR/*.csv" "$LOCAL_PREP_DIR/"

if [ $? -eq 0 ]; then
    echo "Download completed successfully!"
    echo "Files downloaded to: $LOCAL_PREP_DIR"
    echo ""
    echo "Downloaded files:"
    ls -la "$LOCAL_PREP_DIR"/*.csv 2>/dev/null || echo "No CSV files found in $LOCAL_PREP_DIR"
else
    echo "Download failed. Please check:"
    echo "1. WRDS credentials are correct"
    echo "2. prep_on_wrds.sh has been run successfully"
    echo "3. Data files exist in $REMOTE_DATA_DIR on WRDS server"
fi