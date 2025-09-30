# ABOUTME: Downloads VIX volatility index data from FRED API using both VXO and VIX series
# ABOUTME: Creates continuous VIX series and calculates daily VIX changes for market volatility analysis
"""
Inputs:
- FRED API series: VXOCLS (VXO - older volatility series)
- FRED API series: VIXCLS (VIX - current volatility series)

Outputs:
- ../pyData/Intermediate/d_vix.parquet

How to run: python3 VIX.py
"""

import os

import pandas as pd
import requests
from dotenv import load_dotenv

FRED_URL = "https://api.stlouisfed.org/fred/series/observations"
OUTPUT_PATH = "../pyData/Intermediate/d_vix.parquet"

print("=" * 60, flush=True)
print("VIX.py - FRED Volatility Series", flush=True)
print("=" * 60, flush=True)

load_dotenv()
print("Environment variables loaded.", flush=True)


def download_fred_series(series_id, api_key):
    """Pull a single FRED series as a tidy DataFrame."""
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": "1900-01-01",
    }
    response = requests.get(FRED_URL, params=params, timeout=30)
    response.raise_for_status()
    observations = response.json()["observations"]

    # Build DataFrame with parsed dates and numeric values for the requested series
    df = pd.DataFrame(observations)
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.rename(columns={"value": series_id})[["date", series_id]]


print("Downloading VIX data from FRED...", flush=True)
api_key = os.getenv("FRED_API_KEY")

if not api_key:
    # Fail fast so the user knows credentials are missing before making requests
    raise ValueError("FRED_API_KEY not found in environment variables")

vxocls = download_fred_series("VXOCLS", api_key)
vixcls = download_fred_series("VIXCLS", api_key)

print(f"Downloaded {len(vxocls)} VXO observations and {len(vixcls)} VIX observations.", flush=True)

cutoff = pd.Timestamp("2021-09-23")
# Merge both series and take VXO up to the cutoff, VIX afterwards to build a continuous history
vix_data = vxocls.merge(vixcls, on="date", how="outer").sort_values("date")

vix_data["vix"] = vix_data["VXOCLS"]
fill_mask = (vix_data["date"] >= cutoff) & vix_data["VXOCLS"].isna()
vix_data.loc[fill_mask, "vix"] = vix_data.loc[fill_mask, "VIXCLS"]

# Compute daily changes for the blended series and persist to parquet
final_data = vix_data[["date", "vix"]].rename(columns={"date": "time_d"})
final_data["vix"] = final_data["vix"].astype("float32")
final_data["dVIX"] = final_data["vix"].diff().astype("float32")
final_data.to_parquet(OUTPUT_PATH)

date_min = final_data["time_d"].min().date()
date_max = final_data["time_d"].max().date()
print(f"Saved {len(final_data)} rows to {OUTPUT_PATH}", flush=True)
print(f"Date range: {date_min} to {date_max}", flush=True)
print("=" * 60, flush=True)
print("VIX.py completed successfully", flush=True)
print("=" * 60, flush=True)
