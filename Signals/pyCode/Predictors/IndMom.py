# ABOUTME: Calculates industry momentum following Grinblatt and Moskowitz 1999 Table 2A
# ABOUTME: Run from pyCode/ directory: python3 Predictors/IndMom.py

import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "time_avail_m", "ret", "sicCRSP", "mve_c"]].copy()

# SIGNAL CONSTRUCTION

# Convert SIC codes to string and extract first 2 digits for industry grouping
df["sicCRSP"] = df["sicCRSP"].astype(str)
df["sic2D"] = df["sicCRSP"].str[:2]

# Replace missing returns with 0 for momentum calculations
df.loc[df["ret"].isna(), "ret"] = 0

# Sort data for lag operations (ensuring proper panel structure)
df = df.sort_values(["permno", "time_avail_m"])

# Create calendar-based lags for months t-1 to t-5 using time-based merges
for lag in range(1, 6):
    # Create lag data by shifting time_avail_m forward by lag months
    df_lag = df[["permno", "time_avail_m", "ret"]].copy()
    df_lag["time_avail_m"] = df_lag["time_avail_m"] + pd.DateOffset(months=lag)
    df_lag = df_lag.rename(columns={"ret": f"l{lag}_ret"})
    df = df.merge(
        df_lag[["permno", "time_avail_m", f"l{lag}_ret"]],
        on=["permno", "time_avail_m"],
        how="left",
    )

# Compounds monthly returns over months t-5 to t-1 to create individual 6-month momentum
df["Mom6m"] = (
    (1 + df["l1_ret"])
    * (1 + df["l2_ret"])
    * (1 + df["l3_ret"])
    * (1 + df["l4_ret"])
    * (1 + df["l5_ret"])
) - 1


# Calculate industry momentum as market-cap weighted average within 2-digit SIC groups
def calculate_weighted_mean(group):
    # Require both momentum and market value to be valid for weighting
    valid_mask = group["Mom6m"].notna() & group["mve_c"].notna() & (group["mve_c"] > 0)
    if not valid_mask.any():
        return np.nan

    valid_mom = group.loc[valid_mask, "Mom6m"].astype("float64")
    valid_weights = group.loc[valid_mask, "mve_c"].astype("float64")

    # Use higher precision calculation
    numerator = (valid_mom * valid_weights).sum()
    denominator = valid_weights.sum()

    if denominator == 0:
        return np.nan

    return numerator / denominator


# Apply market-cap weighting within each industry-month
group_weighted_means = (
    df.groupby(["sic2D", "time_avail_m"])
    .apply(calculate_weighted_mean, include_groups=False)
    .reset_index()
)
group_weighted_means.columns = ["sic2D", "time_avail_m", "IndMom"]

# Convert to float64 for higher precision
group_weighted_means["IndMom"] = group_weighted_means["IndMom"].astype("float64")

# Assign industry momentum to all firms in each industry-month group
df = df.merge(group_weighted_means, on=["sic2D", "time_avail_m"], how="left")

# SAVE
save_predictor(df, "IndMom")
