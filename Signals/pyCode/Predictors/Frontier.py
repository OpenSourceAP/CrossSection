# ABOUTME: Efficient frontier index following Nguyen and Swanson 2009, Table 4A Spread
# ABOUTME: calculates residual from regression of log(BM) on accounting variables with 60-month rolling window

"""
Frontier.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/Frontier.py
    python3 Predictors/Frontier.py --max-year 1985 (for testing)

Inputs:
    - SignalMasterTable.parquet: Monthly master table with columns [permno, time_avail_m, mve_c, sicCRSP]
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, at, ceq, dltt, capx, sale, xrd, xad, ppent, ebitda]

Outputs:
    - Frontier.csv: CSV file with columns [permno, yyyymm, Frontier]
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import warnings

warnings.filterwarnings("ignore")
import sys
import os
import time
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.sicff import sicff

# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Generate Frontier predictor with optional year filtering"
)
parser.add_argument(
    "--max-year",
    type=int,
    default=None,
    help="Drop data after this year (e.g., 1985 for testing)",
)
args = parser.parse_args()

print(f"Frontier.py starting with max_year={args.max_year}")
start_total = time.time()

# DATA LOAD
print("Loading data...")
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "time_avail_m", "mve_c", "sicCRSP"]].copy()

# Merge with Compustat
comp = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
comp = comp[
    [
        "permno",
        "time_avail_m",
        "at",
        "ceq",
        "dltt",
        "capx",
        "sale",
        "xrd",
        "xad",
        "ppent",
        "ebitda",
    ]
].copy()
df = df.merge(comp, on=["permno", "time_avail_m"], how="inner")

# Apply max_year filter early to reduce data size
if args.max_year:
    print(f"Filtering data to max year {args.max_year}")
    original_len = len(df)
    df = df[df["time_avail_m"].dt.year <= args.max_year].copy()
    filtered_len = len(df)
    print(
        f"Reduced data from {original_len:,} to {filtered_len:,} rows ({100*filtered_len/original_len:.1f}%)"
    )

# Create time_avail as numeric time variable (months since 1960m1)
df["time_avail"] = (df["time_avail_m"].dt.year - 1960) * 12 + (
    df["time_avail_m"].dt.month - 1
)

# SIGNAL CONSTRUCTION
# Replace missing xad with 0
df["xad"] = df["xad"].fillna(0)

# Create variables - handle infinite values by setting to NaN
df["YtempBM"] = np.log(df["mve_c"])
df["YtempBM"] = df["YtempBM"].replace([np.inf, -np.inf], np.nan)

df["tempBook"] = np.log(df["ceq"])
df["tempBook"] = df["tempBook"].replace([np.inf, -np.inf], np.nan)

# Handle division by zero - set to NaN when denominator is 0 or missing
df["tempLTDebt"] = np.where(
    (df["at"] == 0) | df["at"].isna(), np.nan, df["dltt"] / df["at"]
)
df["tempCapx"] = np.where(
    (df["sale"] == 0) | df["sale"].isna(), np.nan, df["capx"] / df["sale"]
)
df["tempRD"] = np.where(
    (df["sale"] == 0) | df["sale"].isna(), np.nan, df["xrd"] / df["sale"]
)
df["tempAdv"] = np.where(
    (df["sale"] == 0) | df["sale"].isna(), np.nan, df["xad"] / df["sale"]
)
df["tempPPE"] = np.where(
    (df["at"] == 0) | df["at"].isna(), np.nan, df["ppent"] / df["at"]
)
df["tempEBIT"] = np.where(
    (df["at"] == 0) | df["at"].isna(), np.nan, df["ebitda"] / df["at"]
)

# Convert sicCRSP for sicff function
print("Computing FF48 industry codes...")
df["tempFF48"] = sicff(df["sicCRSP"], industry=48)
df = df.dropna(subset=["tempFF48"])

# Prepare regression variables
reg_vars = [
    "tempBook",
    "tempLTDebt",
    "tempCapx",
    "tempRD",
    "tempAdv",
    "tempPPE",
    "tempEBIT",
]

# Sort for processing
df = df.sort_values(["permno", "time_avail_m"])

# Initialize predictions column
df["logmefit_NS"] = np.nan

# Process each unique time period
unique_dates = sorted(df["time_avail_m"].unique())
print(
    f"Processing {len(unique_dates)} time periods (starting from {unique_dates[0].strftime('%Y-%m')})..."
)

start_time = time.time()
period_times = []
last_period_time = time.time()
predictions_stored = 0

for i, current_date in enumerate(unique_dates):
    # Convert current_date to time_avail for comparison
    current_time_avail = (current_date.year - 1960) * 12 + (current_date.month - 1)

    # Calendar-based 60 months back
    months_back_60 = current_time_avail - 60

    # Get training data: time_avail <= current AND time_avail > 60 time units back
    train_mask = (df["time_avail"] <= current_time_avail) & (
        df["time_avail"] > months_back_60
    )
    train_data = df[train_mask].copy()
    train_data = train_data.dropna(subset=["YtempBM"] + reg_vars)

    if len(train_data) < 3:  # Require minimal sample size
        continue

    # Get current period data for prediction
    current_mask = df["time_avail_m"] == current_date
    current_data = df[current_mask].copy()
    current_data = current_data.dropna(subset=reg_vars)

    if len(current_data) == 0:
        continue

    try:
        # Create industry dummies for training data
        train_industries = pd.get_dummies(train_data["tempFF48"], prefix="ff48")

        # Prepare training X matrix
        X_train = train_data[reg_vars].copy()
        X_train = pd.concat([X_train, train_industries], axis=1)
        y_train = train_data["YtempBM"]

        # Create industry dummies for current data
        current_industries = pd.get_dummies(current_data["tempFF48"], prefix="ff48")

        # Align columns between training and prediction data
        for col in train_industries.columns:
            if col not in current_industries.columns:
                current_industries[col] = 0
        current_industries = current_industries.reindex(
            columns=train_industries.columns, fill_value=0
        )

        # Prepare prediction X matrix
        X_pred = current_data[reg_vars].copy()
        X_pred = pd.concat([X_pred, current_industries], axis=1)

        # Fit regression using sklearn
        reg = LinearRegression()
        reg.fit(X_train, y_train)

        # Make predictions
        predictions = reg.predict(X_pred)

        # Store predictions back in main dataframe
        # Use the current_data index to properly align predictions
        for idx, pred_value in zip(current_data.index, predictions):
            if df.loc[idx, "time_avail_m"] == current_date:
                df.loc[idx, "logmefit_NS"] = pred_value

        predictions_stored += len(predictions)

    except Exception as e:
        if i % 30 == 0:
            print(f"Failed period {current_date.strftime('%Y-%m')}: {e}")
        continue

    # Track timing and progress
    current_time = time.time()
    period_duration = current_time - last_period_time
    period_times.append(period_duration)
    last_period_time = current_time

    # Keep only last 30 periods for rolling average
    if len(period_times) > 30:
        period_times.pop(0)

    if i % 30 == 0:  # Print progress every 30 periods
        elapsed_time = time.time() - start_time
        if len(period_times) > 0:
            avg_time_per_period = sum(period_times) / len(period_times)
        else:
            avg_time_per_period = elapsed_time / (i + 1)

        periods_remaining = len(unique_dates) - (i + 1)
        estimated_remaining = avg_time_per_period * periods_remaining
        percent_complete = ((i + 1) / len(unique_dates)) * 100

        print(
            f"Processed {i+1}/{len(unique_dates)} periods ({percent_complete:.1f}%), "
            f"stored {len(predictions)} predictions for {current_date.strftime('%Y-%m')}"
        )
        print(
            f"  Elapsed: {elapsed_time:.1f}s, Est. remaining: {estimated_remaining:.1f}s, "
            f"Avg: {avg_time_per_period:.3f}s/period (last {len(period_times)} periods)"
        )

# Calculate Frontier
print(f"Total predictions generated: {predictions_stored}")

df["Frontier"] = df["YtempBM"] - df["logmefit_NS"]
df["Frontier"] = -1 * df["Frontier"]

# Apply filters
print(f"Before ceq filter: {len(df)}")
df = df[(~df["ceq"].isna()) & (df["ceq"] > 0)].copy()
print(f"After ceq filter: {len(df)}")

# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "Frontier"]].copy()
print(f"Before dropping NaN Frontier: {len(df_final)}")
df_final = df_final.dropna(subset=["Frontier"])
print(f"Final output: {len(df_final)} observations")

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "Frontier"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/Frontier.csv")

# Final timing summary
total_time = time.time() - start_total
processing_rate = (
    len(unique_dates) / (time.time() - start_time) if len(unique_dates) > 0 else 0
)
print(f"\nTiming Summary:")
print(f"Total execution time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
print(f"Processed {len(unique_dates)} periods at {processing_rate:.2f} periods/second")
print("Frontier predictor saved successfully")
