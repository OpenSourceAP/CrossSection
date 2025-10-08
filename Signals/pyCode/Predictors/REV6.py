# ABOUTME: REV6 following Chan, Jegadeesh and Lakonishok 1996 JF Table 7
# ABOUTME: calculates 6-month sum of monthly changes in mean earnings estimates scaled by prior month stock price

"""
REV6.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/REV6.py

Inputs:
    - IBES_EPS_Unadj.parquet: IBES earnings forecast data with columns [tickerIBES, time_avail_m, fpi, fpedats, statpers, meanest]
    - SignalMasterTable.parquet: Master security data with columns [permno, tickerIBES, time_avail_m, prc]

Outputs:
    - REV6.csv: CSV file with columns [permno, yyyymm, REV6]
"""

import pandas as pd
import numpy as np

print("Loading and processing REV6...")

# Prepare IBES earnings forecast data
ibes_df = pd.read_parquet("../pyData/Intermediate/IBES_EPS_Unadj.parquet")
ibes_df = ibes_df[ibes_df["fpi"] == "1"].copy()

# Create validity flag for forecasts beyond 30 days from statement period
ibes_df["tmp"] = np.where(
    (ibes_df["fpedats"].notna())
    & (ibes_df["fpedats"] > ibes_df["statpers"] + pd.Timedelta(days=30)),
    1,
    np.nan,
)

# Fill forward estimates when forecast periods match but validity flag missing
ibes_df = ibes_df.sort_values(["tickerIBES", "time_avail_m"])

# Create lagged values for conditional fill-forward logic
ibes_df["meanest_lag1"] = ibes_df.groupby("tickerIBES")["meanest"].shift(1)
ibes_df["fpedats_lag1"] = ibes_df.groupby("tickerIBES")["fpedats"].shift(1)

# Apply fill-forward when validity missing but forecast periods match
fill_condition = (
    pd.isna(ibes_df["tmp"])
    & (ibes_df["fpedats"] == ibes_df["fpedats_lag1"])
    & ibes_df["meanest_lag1"].notna()
)

# Execute conditional estimate replacement
ibes_df.loc[fill_condition, "meanest"] = ibes_df.loc[fill_condition, "meanest_lag1"]

# Remove intermediate calculation columns
ibes_df = ibes_df.drop(["meanest_lag1", "fpedats_lag1"], axis=1)
ibes_df = ibes_df.drop("tmp", axis=1)  # drop tmp

# Note: Missing data handled through conditional fill-forward only

# Load master security table with prices
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "tickerIBES", "time_avail_m", "prc"]].copy()

# Add earnings forecast data to master table
df = df.merge(
    ibes_df[["tickerIBES", "time_avail_m", "meanest"]],
    on=["tickerIBES", "time_avail_m"],
    how="left",
)

# Sort data by firm and time for panel calculations
df = df.sort_values(["permno", "time_avail_m"])

# Calculate monthly forecast revision scaled by lagged stock price
df["meanest_lag1"] = df.groupby("permno")["meanest"].shift(1)
df["prc_lag1"] = df.groupby("permno")["prc"].shift(1)

# Compute price-scaled forecast change
df["tempRev"] = (df["meanest"] - df["meanest_lag1"]) / np.abs(df["prc_lag1"])

# Sum current and 6 lagged monthly revisions for 6-month window
rev6_terms = [df["tempRev"]]  # Current tempRev
for lag in range(1, 7):  # l., l2., l3., l4., l5., l6.
    tempRev_lag = df.groupby("permno")["tempRev"].shift(lag)
    rev6_terms.append(tempRev_lag)

# Organize revision terms for aggregation
rev6_df = pd.DataFrame({f"term_{i}": term for i, term in enumerate(rev6_terms)})

# Sum all 7 revision terms (current plus 6 lags)
# Missing if any component term is missing
df["REV6"] = rev6_df.sum(axis=1, skipna=False)  # NaN if any term is NaN

# Format output variables
df["yyyymm"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month
df["permno"] = df["permno"].astype("int64")
df["yyyymm"] = df["yyyymm"].astype("int64")

df_final = df[["permno", "yyyymm", "REV6"]].copy()
df_final = df_final.dropna(subset=["REV6"])
df_final = df_final.set_index(["permno", "yyyymm"])

# Save predictor to CSV
df_final.to_csv("../pyData/Predictors/REV6.csv")
print("REV6 predictor saved successfully")
