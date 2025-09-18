# ABOUTME: Sales growth over inventory growth following Abarbanell and Bushee 1998, Table 2b RINV
# ABOUTME: calculates the difference between sales growth and inventory growth rates

"""
GrSaleToGrInv.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/

    python3 Predictors/GrSaleToGrInv.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, sale, invt]

Outputs:
    - GrSaleToGrInv.csv: CSV file with columns [permno, yyyymm, GrSaleToGrInv]
    - Primary: ((sale- (.5*(l12.sale + l24.sale)))/(.5*(l12.sale + l24.sale))) - ((invt- (.5*(l12.invt + l24.invt)))/(.5*(l12.invt + l24.invt)))
    - Fallback: ((sale-l12.sale)/l12.sale)-((invt-l12.invt)/l12.invt) if primary is missing
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor


print("Starting GrSaleToGrInv.py...")

# DATA LOAD
print("Loading m_aCompustat data...")

# Load monthly Compustat data with required columns for sales and inventory analysis
m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
if not m_aCompustat_path.exists():
    raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")

df = pd.read_parquet(m_aCompustat_path)

# Keep only the columns we need
required_cols = ["gvkey", "permno", "time_avail_m", "sale", "invt"]
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")

df = df[required_cols].copy()

print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")

# SIGNAL CONSTRUCTION

# Remove duplicate observations for same company-month combination
print("Removing duplicate permno-time_avail_m observations...")
df = df.drop_duplicates(["permno", "time_avail_m"], keep="first")

# Sort data by company and time for time-series calculations
print("Setting up panel data (sorting by permno, time_avail_m)...")
df = df.sort_values(["permno", "time_avail_m"])

# Create 12 and 24-month lags for both sale and invt
print("Calculating 12 and 24-month lags...")

df["l12_sale"] = df.groupby("permno")["sale"].shift(12)
df["l24_sale"] = df.groupby("permno")["sale"].shift(24)
df["l12_invt"] = df.groupby("permno")["invt"].shift(12)
df["l24_invt"] = df.groupby("permno")["invt"].shift(24)

# Primary calculation: difference between sales and inventory growth rates using 12/24-month average baselines
print("Calculating primary GrSaleToGrInv formula...")

# Calculate average of 12 and 24-month lags
df["avg_l12_l24_sale"] = 0.5 * (df["l12_sale"] + df["l24_sale"])
df["avg_l12_l24_invt"] = 0.5 * (df["l12_invt"] + df["l24_invt"])

# Calculate sales growth component
df["sale_growth"] = np.where(
    df["avg_l12_l24_sale"] == 0,
    np.nan,  # Division by zero = missing
    (df["sale"] - df["avg_l12_l24_sale"]) / df["avg_l12_l24_sale"],
)

# Calculate inventory growth component
df["invt_growth"] = np.where(
    df["avg_l12_l24_invt"] == 0,
    np.nan,  # Division by zero = missing
    (df["invt"] - df["avg_l12_l24_invt"]) / df["avg_l12_l24_invt"],
)

# Primary GrSaleToGrInv calculation
df["GrSaleToGrInv"] = df["sale_growth"] - df["invt_growth"]

# Fallback calculation: use 12-month growth rates when primary calculation is unavailable
print("Applying fallback formula for missing values...")

# Calculate fallback components
df["sale_growth_12m"] = np.where(
    df["l12_sale"] == 0,
    np.nan,  # Division by zero = missing
    (df["sale"] - df["l12_sale"]) / df["l12_sale"],
)

df["invt_growth_12m"] = np.where(
    df["l12_invt"] == 0,
    np.nan,  # Division by zero = missing
    (df["invt"] - df["l12_invt"]) / df["l12_invt"],
)

df["GrSaleToGrInv_fallback"] = df["sale_growth_12m"] - df["invt_growth_12m"]

# Use fallback values when primary calculation yields missing values
df["GrSaleToGrInv"] = np.where(
    df["GrSaleToGrInv"].isna(), df["GrSaleToGrInv_fallback"], df["GrSaleToGrInv"]
)

print(f"Calculated GrSaleToGrInv for {df['GrSaleToGrInv'].notna().sum()} observations")

# Clean up intermediate columns
df = df[["gvkey", "permno", "time_avail_m", "GrSaleToGrInv"]].copy()

# SAVE
# Save standardized predictor output
save_predictor(df, "GrSaleToGrInv")

print("GrSaleToGrInv.py completed successfully")
