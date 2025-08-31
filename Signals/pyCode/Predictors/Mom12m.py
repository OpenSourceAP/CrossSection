# ABOUTME: Calculates 12-month momentum following Jegadeesh and Titman 1993 Table 1A K=3 row 12
# ABOUTME: Run from pyCode/ directory: python3 Predictors/Mom12m.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/Mom12m.csv

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_replication import stata_multi_lag
from utils.save_standardized import save_predictor

print("=" * 80)
print("🏗️  Mom12m.py")
print("Creating twelve-month momentum predictor")
print("=" * 80)

# DATA LOAD
print("📊 Loading SignalMasterTable data...")
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()
print(f"Loaded: {len(df):,} observations")

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
print("🧮 Computing 12-month momentum signal...")
# Replace missing returns with 0 for momentum calculations
df['ret'] = df['ret'].fillna(0)

# Create 11 monthly lags (t-1 to t-11) using calendar-aware lag function
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

# Compounds monthly returns over months t-11 to t-1 to create 12-month momentum (skips current month t)
df['Mom12m'] = ((1 + df['ret_lag1']) *
                (1 + df['ret_lag2']) *
                (1 + df['ret_lag3']) *
                (1 + df['ret_lag4']) *
                (1 + df['ret_lag5']) *
                (1 + df['ret_lag6']) *
                (1 + df['ret_lag7']) *
                (1 + df['ret_lag8']) *
                (1 + df['ret_lag9']) *
                (1 + df['ret_lag10']) *
                (1 + df['ret_lag11'])) - 1


# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'Mom12m']].copy()

# SAVE
print("💾 Saving Mom12m predictor...")
save_predictor(df_final, 'Mom12m')
print("✅ Mom12m.csv saved successfully")

print("=" * 80)
print("✅ Mom12m.py Complete")
print("Twelve-month momentum predictor generated successfully")
print("=" * 80)