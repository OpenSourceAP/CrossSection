# ABOUTME: Revenue Growth Rank following Lakonishok, Shleifer, Vishny 1994, Table 6 panel 2
# ABOUTME: calculates weighted average of revenue growth ranks over past 5 years
"""
MeanRankRevGrowth.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/MeanRankRevGrowth.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, revt]

Outputs:
    - MeanRankRevGrowth.csv: CSV file with columns [permno, yyyymm, MeanRankRevGrowth]
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df[["gvkey", "permno", "time_avail_m", "revt"]].copy()

# Drop duplicates
df = df.drop_duplicates(subset=["permno", "time_avail_m"])

# Sort for lag operations
df = df.sort_values(["permno", "time_avail_m"])

# SIGNAL CONSTRUCTION
# Calculate 12-month revenue growth using calendar-based lag
df_revt = df[["permno", "time_avail_m", "revt"]].copy()
df["time_lag12_revt"] = df["time_avail_m"] - pd.DateOffset(months=12)
df = df.merge(
    df_revt.rename(columns={"time_avail_m": "time_lag12_revt", "revt": "revt_lag12"}),
    on=["permno", "time_lag12_revt"],
    how="left",
)
df = df.drop("time_lag12_revt", axis=1)

# Replicate Stata's log behavior: log of zero/negative is missing
valid_mask = (
    (df["revt"] > 0)
    & (df["revt_lag12"] > 0)
    & df["revt"].notna()
    & df["revt_lag12"].notna()
)
df["temp"] = np.nan
df.loc[valid_mask, "temp"] = np.log(df.loc[valid_mask, "revt"]) - np.log(
    df.loc[valid_mask, "revt_lag12"]
)

# Create monthly rankings using Stata's exact method
# gsort time_avail_m -temp
df = df.sort_values(
    ["time_avail_m", "temp"], ascending=[True, False], na_position="last"
)

# Generate within-month ranking for non-missing temp values
df["tempRank"] = np.nan
df["row_num"] = df.groupby("time_avail_m").cumcount() + 1
df.loc[df["temp"].notna(), "tempRank"] = df.loc[df["temp"].notna(), "row_num"]
df = df.drop("row_num", axis=1)

# Sort back for lag operations
df = df.sort_values(["permno", "time_avail_m"])

# Calculate calendar-based lagged ranks (not positional shift)
# Create a copy for merging
df_ranks = df[["permno", "time_avail_m", "tempRank"]].copy()

# Calculate lag times
df["time_lag12"] = df["time_avail_m"] - pd.DateOffset(months=12)
df["time_lag24"] = df["time_avail_m"] - pd.DateOffset(months=24)
df["time_lag36"] = df["time_avail_m"] - pd.DateOffset(months=36)
df["time_lag48"] = df["time_avail_m"] - pd.DateOffset(months=48)
df["time_lag60"] = df["time_avail_m"] - pd.DateOffset(months=60)

# Merge to get lagged ranks
df = df.merge(
    df_ranks.rename(
        columns={"time_avail_m": "time_lag12", "tempRank": "tempRank_lag12"}
    ),
    on=["permno", "time_lag12"],
    how="left",
)
df = df.merge(
    df_ranks.rename(
        columns={"time_avail_m": "time_lag24", "tempRank": "tempRank_lag24"}
    ),
    on=["permno", "time_lag24"],
    how="left",
)
df = df.merge(
    df_ranks.rename(
        columns={"time_avail_m": "time_lag36", "tempRank": "tempRank_lag36"}
    ),
    on=["permno", "time_lag36"],
    how="left",
)
df = df.merge(
    df_ranks.rename(
        columns={"time_avail_m": "time_lag48", "tempRank": "tempRank_lag48"}
    ),
    on=["permno", "time_lag48"],
    how="left",
)
df = df.merge(
    df_ranks.rename(
        columns={"time_avail_m": "time_lag60", "tempRank": "tempRank_lag60"}
    ),
    on=["permno", "time_lag60"],
    how="left",
)

# Clean up temporary columns
df = df.drop(
    ["time_lag12", "time_lag24", "time_lag36", "time_lag48", "time_lag60"], axis=1
)

# Calculate weighted average rank
df["MeanRankRevGrowth"] = (
    5 * df["tempRank_lag12"]
    + 4 * df["tempRank_lag24"]
    + 3 * df["tempRank_lag36"]
    + 2 * df["tempRank_lag48"]
    + df["tempRank_lag60"]
) / 15

# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "MeanRankRevGrowth"]].copy()
df_final = df_final.dropna(subset=["MeanRankRevGrowth"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "MeanRankRevGrowth"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/MeanRankRevGrowth.csv")

print("MeanRankRevGrowth predictor saved successfully")
