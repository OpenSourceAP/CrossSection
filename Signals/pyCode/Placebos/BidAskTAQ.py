# ABOUTME: BidAskTAQ.py - renames hf_spread to BidAskTAQ placebo
# ABOUTME: Python equivalent of BidAskTAQ.do, translates line-by-line from Stata code

"""
BidAskTAQ.py

Inputs:
    - hf_spread.parquet: permno, time_avail_m, hf_spread columns

Outputs:
    - BidAskTAQ.csv: permno, yyyymm, BidAskTAQ columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/BidAskTAQ.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting BidAskTAQ.py")

# DATA LOAD
# use "$pathDataIntermediate/hf_spread", clear
print("Loading hf_spread...")
df = pl.read_parquet("../pyData/Intermediate/hf_spread.parquet")

print(f"After loading hf_spread: {len(df)} rows")

# SIGNAL CONSTRUCTION
# rename hf_spread BidAskTAQ
print("Renaming hf_spread to BidAskTAQ...")
df = df.rename({'hf_spread': 'BidAskTAQ'})

print(f"Generated BidAskTAQ for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'BidAskTAQ'])

# SAVE
# do "$pathCode/saveplacebo" BidAskTAQ
save_placebo(df_final, 'BidAskTAQ')

print("BidAskTAQ.py completed")