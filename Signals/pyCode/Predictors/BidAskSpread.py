# ABOUTME: BidAskSpread.py - loads BidAskSpread predictor from pre-computed data
# ABOUTME: Processes bid-ask spread data using Corwin-Schultz methodology

"""
BidAskSpread.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/BidAskSpread.py

Inputs:
    - BAspreadsCorwin.parquet: Pre-computed bid-ask spreads from Corwin-Schultz methodology

Outputs:
    - BidAskSpread.csv: CSV file with columns [permno, yyyymm, BidAskSpread]
    - BidAskSpread data is pre-computed using SAS code (Corwin_Schultz_Edit.sas)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor


print("Starting BidAskSpread.py...")

# DATA LOAD
print("Loading BAspreadsCorwin data...")

# Load pre-computed bid-ask spreads data
ba_spreads_path = Path("../pyData/Intermediate/BAspreadsCorwin.parquet")
if not ba_spreads_path.exists():
    raise FileNotFoundError(f"Required input file not found: {ba_spreads_path}")

df = pd.read_parquet(ba_spreads_path)

print(f"Loaded BAspreadsCorwin: {df.shape[0]} rows, {df.shape[1]} columns")

# SIGNAL CONSTRUCTION

# * Construction is done in SAS code (Corwin_Schultz_Edit.sas)
# The BidAskSpread variable should already exist in the data

if 'BidAskSpread' not in df.columns:
    raise ValueError("BidAskSpread column not found in input data")

print(f"BidAskSpread available for {df['BidAskSpread'].notna().sum()} observations")

# SAVE
# Save BidAskSpread predictor to standardized format
save_predictor(df, 'BidAskSpread')

print("BidAskSpread.py completed successfully")