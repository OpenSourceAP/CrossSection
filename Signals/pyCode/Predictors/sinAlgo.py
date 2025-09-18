# ABOUTME: Sin Stock predictor following Hong and Kacperczyk 2009, Table 4A 1965-2006 first row, Table 4B 1926-2006 first row
# ABOUTME: Binary variable = 1 for firms with segments in sin industries (alcohol, tobacco, gaming), 0 for comparable stocks
"""
Usage:
    python3 Predictors/sinAlgo.py

Inputs:
    - CompustatSegments.parquet: Segment data with SIC/NAICS codes
    - SignalMasterTable.parquet: Monthly master table with firm identifiers
    - m_aCompustat.parquet: Monthly Compustat data

Outputs:
    - sinAlgo.csv: CSV file with columns [permno, yyyymm, sinAlgo]
    - sinAlgo = 1 for sin stocks, 0 for comparable stocks, missing otherwise
"""

import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.sicff import sicff

print("Starting sinAlgo.py...")

# DATA LOAD (Compustat Segments)
print("Loading Compustat segments data...")
segments = pd.read_parquet("../pyData/Intermediate/CompustatSegments.parquet")
segments = segments[["gvkey", "sics1", "naicsh", "datadate"]].copy()
segments["year"] = segments["datadate"].dt.year
print(f"Loaded segments data: {segments.shape[0]} rows")

# SIGNAL CONSTRUCTION
print("Identifying sin segments...")
segments["sinSegTobacco"] = np.nan
segments["sinSegBeer"] = np.nan
segments["sinSegGaming"] = np.nan

# Identify tobacco segments by SIC codes 2100-2199
tobacco_mask = (segments["sics1"] >= 2100) & (segments["sics1"] <= 2199)
segments.loc[tobacco_mask, "sinSegTobacco"] = 1

# Identify beer segments by SIC codes 2080-2085
beer_mask = (segments["sics1"] >= 2080) & (segments["sics1"] <= 2085)
segments.loc[beer_mask, "sinSegBeer"] = 1

# Identify gaming segments by specific NAICS codes
gaming_codes = [7132, 71312, 713210, 71329, 713290, 72112, 721120]
gaming_mask = segments["naicsh"].isin(gaming_codes)
segments.loc[gaming_mask, "sinSegGaming"] = 1

# Create indicator for any sin segment (tobacco, beer, or gaming)
any_mask = (
    (segments["sinSegTobacco"] == 1)
    | (segments["sinSegBeer"] == 1)
    | (segments["sinSegGaming"] == 1)
)
segments["sinSegAny"] = np.nan
segments.loc[any_mask, "sinSegAny"] = 1

# Keep only segments identified as sin stocks
segments = segments[segments["sinSegAny"] == 1].copy()

# Aggregate to firm-year level, taking maximum across segments
seg_collapsed = (
    segments.groupby(["gvkey", "year"])
    .agg(
        {
            "sinSegTobacco": "max",
            "sinSegBeer": "max",
            "sinSegGaming": "max",
            "sinSegAny": "max",
        }
    )
    .reset_index()
)

# Save temp file equivalent
temp = seg_collapsed.copy()

# Apply historical backfill rule: stocks identified as sinful remain sinful throughout history
first_year = temp.groupby("gvkey").first().reset_index()
# Store first year when sin classification was identified
first_year = first_year.rename(columns={"year": "firstYear"})
# Mark these as first-year sin classifications for backfilling
first_year = first_year.rename(
    columns={
        "sinSegTobacco": "sinSegTobaccoFirstYear",
        "sinSegBeer": "sinSegBeerFirstYear",
        "sinSegGaming": "sinSegGamingFirstYear",
        "sinSegAny": "sinSegAnyFirstYear",
    }
)

# DATA LOAD (Firm-level industry codes)
print("Loading SignalMasterTable...")
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "gvkey", "time_avail_m", "sicCRSP", "shrcd"]].copy()
print(f"Loaded SignalMasterTable: {df.shape[0]} rows")

# Add NAICS codes from Compustat annual data
print("Merging with Compustat annual data...")
comp = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
comp = comp[["permno", "time_avail_m", "naicsh"]].copy()
df = df.merge(comp, on=["permno", "time_avail_m"], how="left")
print(f"After merge: {df.shape[0]} rows")

# Extract year from time_avail_m date
df["year"] = df["time_avail_m"].dt.year
# Convert SIC codes to numeric
df["sicCRSP"] = pd.to_numeric(df["sicCRSP"], errors="coerce")

# SIGNAL CONSTRUCTION
print("Identifying sin stocks...")
df["sinStockTobacco"] = np.nan
df["sinStockBeer"] = np.nan
df["sinStockGaming"] = np.nan

# Identify tobacco stocks by CRSP SIC codes 2100-2199 (only from 1965 onwards per footnote 14)
tobacco_stock_mask = (
    (df["sicCRSP"] >= 2100) & (df["sicCRSP"] <= 2199) & (df["year"] >= 1965)
)
df.loc[tobacco_stock_mask, "sinStockTobacco"] = 1

# Identify beer stocks by CRSP SIC codes 2080-2085
beer_stock_mask = (df["sicCRSP"] >= 2080) & (df["sicCRSP"] <= 2085)
df.loc[beer_stock_mask, "sinStockBeer"] = 1

# Identify gaming stocks by specific NAICS codes
gaming_stock_mask = df["naicsh"].isin(gaming_codes)
df.loc[gaming_stock_mask, "sinStockGaming"] = 1

# Create indicator for any sin stock classification
stock_any_mask = (
    (df["sinStockTobacco"] == 1)
    | (df["sinStockBeer"] == 1)
    | (df["sinStockGaming"] == 1)
)
df["sinStockAny"] = np.nan
df.loc[stock_any_mask, "sinStockAny"] = 1

# Comparison group (top of page 22, FF48 groups 2, 3, 7, 43)
# Map SIC codes to Fama-French 48 industry classifications
df["tmpFF48"] = df["sicCRSP"].apply(
    lambda x: sicff(x, industry=48) if pd.notna(x) else np.nan
)
# Create comparison group using FF48 industries 2, 3, 7, 43 (per page 22)
comparable_mask = df["tmpFF48"].isin([2, 3, 7, 43])
df["ComparableStock"] = np.nan
df.loc[comparable_mask, "ComparableStock"] = 1

# Add segment-level sin classifications by firm-year
df = df.merge(temp, on=["gvkey", "year"], how="left")

# Add first-year sin classifications for historical backfill
df = df.merge(first_year, on="gvkey", how="left")

print("Calculating sinAlgo signal...")
# Finally, create sin stock indicator
df["sinAlgo"] = np.nan

# Create final sin algorithm indicator based on multiple criteria:
# 1. Current stock-level classification
# 2. Current segment-level classification
# 3. Historical backfill for tobacco (1965+)
# 4. Historical backfill for beer/gaming (all years, pre-1965 gaming only)

# Breaking down the complex condition
condition1 = df["sinStockAny"] == 1
condition2 = df["sinSegAny"] == 1
condition3 = (
    (df["sinSegAnyFirstYear"] == 1)
    & (df["year"] < df["firstYear"])
    & (df["year"] >= 1965)
)
# Apply operator precedence: beer classification OR (gaming AND historical AND pre-1965)
condition4a = df["sinSegBeerFirstYear"] == 1
condition4b = (
    (df["sinSegGamingFirstYear"] == 1)
    & (df["year"] < df["firstYear"])
    & (df["year"] < 1965)
)
condition4 = condition4a | condition4b

sin_mask = condition1 | condition2 | condition3 | condition4
df.loc[sin_mask, "sinAlgo"] = 1

# Assign non-sin classification to comparable stocks not already classified as sin
comparable_not_sin_mask = (df["ComparableStock"] == 1) & df["sinAlgo"].isna()
df.loc[comparable_not_sin_mask, "sinAlgo"] = 0

# Exclude non-standard share classes (shrcd > 11)
df.loc[df["shrcd"] > 11, "sinAlgo"] = np.nan

# SAVE
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor

# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "sinAlgo"]].copy()
print(f"Calculated sinAlgo for {df_final['sinAlgo'].notna().sum()} observations")

# SAVE using standard savepredictor format
save_predictor(df_final, "sinAlgo")
print("sinAlgo.py completed successfully")
