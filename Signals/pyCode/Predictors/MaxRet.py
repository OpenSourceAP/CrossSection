# ABOUTME: Maximum return following Bali, Cakici, and Whitelaw 2011, Table 1 VW 10-1
# ABOUTME: calculates maximum of daily returns over the previous month

# Run from pyCode/ directory
# Inputs: dailyCRSP.parquet
# Output: ../pyData/Predictors/MaxRet.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
df = df[["permno", "time_d", "ret"]].copy()

# SIGNAL CONSTRUCTION
# Convert daily date to monthly
df["time_avail_m"] = pd.to_datetime(df["time_d"]).dt.to_period("M").dt.to_timestamp()

# Calculate maximum return by permno-month
df_final = df.groupby(["permno", "time_avail_m"])["ret"].max().reset_index()
df_final = df_final.rename(columns={"ret": "MaxRet"})

# Drop missing values
df_final = df_final.dropna(subset=["MaxRet"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "MaxRet"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/MaxRet.csv")

print("MaxRet predictor saved successfully")
