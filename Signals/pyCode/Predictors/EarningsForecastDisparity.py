# ABOUTME: EarningsForecastDisparity.py - computes long-vs-short EPS forecasts (Da and Warachka 2011 JFE Table 2B)
# ABOUTME: Calculates disparity between long-term growth forecasts and scaled short-term earnings expectations

# Usage: python3 EarningsForecastDisparity.py
# Inputs: IBES EPS forecasts, master table, and actual earnings data
# Output: Long-term vs short-term forecast disparity measure

import pandas as pd
import numpy as np

# Prepare IBES forecast data
# Extract 1-year ahead earnings forecasts
ibes_eps = pd.read_parquet("../pyData/Intermediate/IBES_EPS_Unadj.parquet")
tempIBESshort = ibes_eps[ibes_eps["fpi"] == "1"].copy()
tempIBESshort = tempIBESshort[
    (tempIBESshort["fpedats"].notna())
    & (tempIBESshort["fpedats"] > tempIBESshort["statpers"] + pd.Timedelta(days=30))
]

# Extract long-term growth forecasts (5-year ahead)
tempIBESlong = ibes_eps[ibes_eps["fpi"] == "0"].copy()
tempIBESlong = tempIBESlong.rename(columns={"meanest": "fgr5yr"})

print("Starting EarningsForecastDisparity.py...")

# Load master security table with identifiers
signal_master = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m", "tickerIBES"],
)

# Merge short-term forecasts (left join preserves all securities)
df = pd.merge(
    signal_master,
    tempIBESshort[["tickerIBES", "time_avail_m", "meanest"]],
    on=["tickerIBES", "time_avail_m"],
    how="left",
    validate="m:1",
)

# Merge long-term forecasts (left join preserves all securities)
df = pd.merge(
    df,
    tempIBESlong[["tickerIBES", "time_avail_m", "fgr5yr"]],
    on=["tickerIBES", "time_avail_m"],
    how="left",
    validate="m:1",
)

# Add actual earnings data for scaling
ibes_actuals = pd.read_parquet(
    "../pyData/Intermediate/IBES_UnadjustedActuals.parquet",
    columns=["tickerIBES", "time_avail_m", "fy0a"],
)
df = pd.merge(
    df, ibes_actuals, on=["tickerIBES", "time_avail_m"], how="left", validate="m:1"
)

# Compute scaled short-term forecast error
# Scale by absolute value of actual earnings to avoid sign issues
df["tempShort"] = np.where(
    df["fy0a"] == 0, np.nan, 100 * (df["meanest"] - df["fy0a"]) / abs(df["fy0a"])
)

# Compute disparity between long-term growth and short-term scaled forecast
df["EarningsForecastDisparity"] = df["fgr5yr"] - df["tempShort"]

# Convert date to YYYYMM format
df["yyyymm"] = (df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month).astype(
    int
)

# Prepare final output with valid observations only
result = df[["permno", "yyyymm", "EarningsForecastDisparity"]].dropna(
    subset=["EarningsForecastDisparity"]
)

# Save predictor to CSV
result.to_csv("../pyData/Predictors/EarningsForecastDisparity.csv", index=False)
