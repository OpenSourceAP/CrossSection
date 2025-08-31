# ABOUTME: Calculates customer momentum following Cohen and Frazzini 2008 Table 3A
# ABOUTME: Run: python3 pyCode/Predictors/CustomerMomentum.py

"""
CustomerMomentum Predictor

Customer momentum calculation (data constructed externally).

Inputs:
- customerMom.parquet (custmom data constructed externally)

Outputs:
- CustomerMomentum.csv (permno, yyyymm, CustomerMomentum)

This predictor simply loads the customerMom dataset and renames the column.
Note: The signal is constructed in R4_CustomerMomentum.R
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

print("Starting CustomerMomentum predictor...")

# DATA LOAD
print("Loading customerMom data...")
df = pd.read_parquet('../pyData/Intermediate/customerMom.parquet')

print(f"Loaded {len(df):,} customerMom observations")

# SIGNAL CONSTRUCTION
print("Constructing CustomerMomentum signal...")

# Rename custmom to CustomerMomentum
df = df.rename(columns={'custmom': 'CustomerMomentum'})

print(f"Generated CustomerMomentum values for {df['CustomerMomentum'].notna().sum():,} observations")

# SAVE
print("Saving predictor...")
save_predictor(df, 'CustomerMomentum')

print("CustomerMomentum predictor completed successfully!")