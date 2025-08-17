# Debug Plan for MS Predictor - Precision Failures

## Task Overview
Debug precision failures in MS.py by comparing Python output with Stata log MS.log using checkpoint analysis. Focus on permno 11170 in 1995-1996 period as the debug case.

## Key Issue Analysis
The Stata log shows missing values (.) for key metrics like ROA, CFROA, niVol, and revVol for permno 11170, but the final binary indicators (m1-m8) are all 0, and tempMS/MS = 0 → 1. The Python code may be handling missing values differently.

## Step-by-Step Debug Plan

### 1. Run and Test Current State
**Exact commands to run:**
```bash
cd pyCode/
source .venv/bin/activate
python3 Predictors/MS.py
python3 utils/test_predictors.py --predictors MS
```

**Expected output:** Record the test results showing precision failure details.

### 2. Compare Checkpoint Data
**Write debug script:** Create `Debug/debug_ms_checkpoints.py` with this exact content:
```python
import polars as pl
import pandas as pd

# Load the generated data
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
smt = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")

# Recreate the exact merge logic from MS.py lines 80-85
merged = (df.select(["permno", "gvkey", "time_avail_m", "datadate", "at", "ceq", "ni", "oancf", "fopt", "wcapch", "ib", "dp", "xrd", "capx", "xad", "revt"])
    .unique(["permno", "time_avail_m"], keep="first")
    .join(smt.select(["permno", "time_avail_m", "mve_c", "sicCRSP"]), on=["permno", "time_avail_m"], how="inner")
    .join(qcomp.select(["gvkey", "time_avail_m", "niq", "atq", "saleq", "oancfy", "capxy", "xrdq", "fyearq", "fqtr", "datafqtr", "datadateq"]), on=["gvkey", "time_avail_m"], how="left")
)

# Check permno 11170 data availability
debug_data = merged.filter(
    (pl.col("permno") == 11170) & 
    (pl.col("time_avail_m").dt.year() >= 1995) & 
    (pl.col("time_avail_m").dt.year() <= 1996)
).select(["permno", "time_avail_m", "niq", "atq", "oancfy", "capxy", "xrdq", "fqtr"])

print("Python quarterly data for permno 11170:")
print(debug_data.to_pandas().to_string(index=False))

# Check if quarterly data is available at all
q_data_check = qcomp.filter(pl.col("gvkey").is_in(merged.filter(pl.col("permno") == 11170)["gvkey"].unique()))
print(f"\nAll quarterly data for gvkey(s) of permno 11170: {len(q_data_check)} rows")
```

**Compare with Stata log:** The Stata log shows ROA and CFROA are missing (.) for permno 11170, suggesting quarterly aggregation issues.

### 3. Hypothesis 1: Quarterly Aggregation Logic
**Problem location:** Lines 164-177 in MS.py - quarterly rolling aggregation logic.

**Issue:** Python `rolling_mean(window_size=12, min_samples=12)` vs Stata `asrol ... window(time_avail_m 12) min(12)` may behave differently with irregular quarterly data.

**Debug script:** Add to `Debug/debug_ms_checkpoints.py`:
```python
# Test quarterly aggregation for permno 11170
test_perm = merged.filter(pl.col("permno") == 11170).sort("time_avail_m")

# Check raw quarterly data availability
print("Raw quarterly data for permno 11170:")
q_cols = ["time_avail_m", "niq", "xrdq", "oancfy", "capxy", "fqtr"]
print(test_perm.select(q_cols).to_pandas().to_string(index=False))

# Test the rolling aggregation step by step
test_with_agg = test_perm.with_columns([
    pl.col("niq").rolling_mean(window_size=12, min_samples=12).over("permno").mul(4).alias("niqsum_py"),
    pl.col("oancfy").rolling_mean(window_size=12, min_samples=12).over("permno").mul(4).alias("oancfysum_py")
])

print("\nAfter rolling aggregation:")
print(test_with_agg.select(["time_avail_m", "niq", "niqsum_py", "oancfy", "oancfysum_py"]).to_pandas().to_string(index=False))
```

### 4. Hypothesis 2: Missing Data in Quarterly Variables
**Problem location:** Lines 72-76 in MS.py - quarterly data loading and merging.

**Issue:** The left join may not be finding matching quarterly data for permno 11170, causing all quarterly variables to be null.

**Debug test:** Add gvkey consistency check:
```python
# Check gvkey matching between annual and quarterly data
annual_gvkeys = df.filter(pl.col("permno") == 11170)["gvkey"].unique()
quarterly_gvkeys = qcomp["gvkey"].unique()
print(f"Annual gvkeys for permno 11170: {annual_gvkeys.to_list()}")
print(f"Quarterly data has these gvkeys: {len(quarterly_gvkeys)} total")
print(f"Overlap: {set(annual_gvkeys.to_list()).intersection(set(quarterly_gvkeys.to_list()))}")
```

### 5. Hypothesis 3: Time Period Mismatch
**Problem location:** Lines 164-185 in MS.py - quarterly data handling for 1995-1996.

**Issue:** The 1988 cutoff logic (line 180-185) may interfere with quarterly aggregation, or early years may lack sufficient quarterly history.

**Debug test:** Check data availability by year:
```python
# Check quarterly data coverage by year for permno 11170
coverage = merged.filter(pl.col("permno") == 11170).with_columns([
    pl.col("time_avail_m").dt.year().alias("year"),
    pl.col("niq").is_not_null().alias("has_niq"),
    pl.col("oancfy").is_not_null().alias("has_oancfy")
]).group_by("year").agg([
    pl.col("has_niq").sum().alias("niq_count"),
    pl.col("has_oancfy").sum().alias("oancfy_count"),
    pl.len().alias("total_obs")
])
print("Quarterly data coverage by year:")
print(coverage.to_pandas().to_string(index=False))
```

### 6. Fix Implementation
**Once hypothesis is confirmed:**

**If Hypothesis 1 (rolling aggregation):** 
- Edit lines 168-177 in MS.py
- Change from `rolling_mean(window_size=12, min_samples=12)` to a time-aware aggregation that matches Stata's `asrol` behavior
- Ensure the window is calendar-based, not position-based

**If Hypothesis 2 (missing quarterly data):**
- Edit lines 72-76 in MS.py  
- Add data validation after quarterly merge
- Potentially change join strategy or add fallback logic

**If Hypothesis 3 (time period issues):**
- Edit lines 180-185 in MS.py
- Modify the 1988 cutoff logic to not interfere with quarterly aggregation
- Add explicit early-year handling

### 7. Test Fix
**After each edit:**
```bash
cd pyCode/
python3 Predictors/MS.py
python3 utils/test_predictors.py --predictors MS
```

**Success criteria:** 
- CHECKPOINT 2 in Python output shows non-missing ROA and CFROA values for permno 11170
- Test passes with >99% precision match to Stata

## Critical Files to Edit
- **Primary:** `/Users/chen1678/Library/CloudStorage/Dropbox/oap-ac/CrossSection/Signals/pyCode/Predictors/MS.py`
- **Debug scripts:** `/Users/chen1678/Library/CloudStorage/Dropbox/oap-ac/CrossSection/Signals/pyCode/Debug/debug_ms_checkpoints.py` (create new)

## Key Debugging Focus
The core issue appears to be in the quarterly data aggregation step (lines 164-177) where Python's rolling operations may not match Stata's `asrol` behavior, particularly for irregular time series data or insufficient historical data.