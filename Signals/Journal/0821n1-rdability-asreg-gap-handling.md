# 0821n1-rdability-asreg-gap-handling.md

## Issue
RDAbility.py produces different regression coefficients than Stata for asreg calculations.

## Root Cause Discovery
After extensive debugging on permno 79283 (gvkey 28504), discovered the issue is related to **missing year gaps** in the data.

### Key Finding
**Stata's asreg correctly handles missing years in panel data, while Python's shift() does not.**

## Specific Example
For gvkey 28504:
- Years present: 1993, 1994, **[1995 MISSING]**, 1996, 1997, 1998, 1999, 2000, 2001, ...
- When calculating tempY = log(sale / lag(sale))
  - Python shift(1) incorrectly uses 1994 data for 1996's lag
  - Stata correctly identifies that 1996's lag calculation spans a gap

### Evidence
For year 2001 regression window (1994-2001):
- **Python**: Uses all 7 observations → coefficient = -51.266108
- **Stata**: Excludes year 1996 (invalid lag) → coefficient = -59.618244

When we manually exclude year 1996 in Python:
```python
# Excluding year 1996: 6 observations
# Regression coefficient: -59.618243
# Stata coefficient:     -59.618244
# Match: YES!
```

## The Problem with shift()
```python
# Current (WRONG) approach:
df.with_columns([
    (pl.col("tempSale") / pl.col("tempSale").shift(1).over("gvkey")).log().alias("tempY")
])

# This uses position-based lag, not time-based lag
# When year 1995 is missing:
#   Year 1996's lag incorrectly points to 1994
#   This creates tempY = log(sale_1996 / sale_1994) 
#   Should be: tempY = null (because sale_1995 is missing)
```

## Solution Approaches

### Option 1: Detect Year Gaps
Check if the previous fyear is exactly fyear - 1:
```python
df = df.with_columns([
    pl.col("fyear").shift(1).over("gvkey").alias("prev_fyear")
])

# Only calculate tempY when there's no gap
df = df.with_columns([
    pl.when(pl.col("fyear") - pl.col("prev_fyear") == 1)
    .then((pl.col("tempSale") / pl.col("tempSale").shift(1).over("gvkey")).log())
    .otherwise(None)
    .alias("tempY")
])
```

### Option 2: Time-Based Lag (More Robust)
Use actual fyear values for merging:
```python
# Create lagged data
lag_df = df.select(["gvkey", "fyear", "tempSale"])
lag_df = lag_df.with_columns([
    (pl.col("fyear") + 1).alias("fyear"),
    pl.col("tempSale").alias("lag_tempSale")
])

# Merge to get proper time-based lag
df = df.join(
    lag_df, 
    on=["gvkey", "fyear"], 
    how="left"
)

# Calculate tempY with proper lag
df = df.with_columns([
    (pl.col("tempSale") / pl.col("lag_tempSale")).log().alias("tempY")
])
```

## Impact on asreg and asrol

This affects:
1. **asreg calculations**: Invalid lag observations should be excluded from regression windows
2. **asrol calculations**: The tempMean values are different because Stata excludes invalid observations

### tempMean Discrepancy Explained
- Stata shows tempMean = 0.857143 (6/7) for year 2002
- Python shows tempMean = 1.0 (7/7)
- Difference: Stata excludes year 1996 from the window due to invalid lag

## Broader Implications

This issue likely affects **ALL predictors** that use:
- Lag operators (l., l2., etc.)
- Panel data with gaps
- asreg with lagged variables

## Testing Validation

To verify the fix:
1. Apply gap detection to tempY calculation
2. Exclude observations with invalid lags from asreg windows
3. Recalculate tempMean excluding invalid observations
4. Compare coefficients with Stata output

## Specific Code Lines Affected in RDAbility.py

Lines that need modification:
- Line creating tempY (uses shift without gap detection)
- Lines running asreg (should exclude invalid lag observations)
- Lines calculating tempMean (should match Stata's exclusion logic)

## Specific Stata Lines That Are Not Replicating

### Line 56: `gen tempY = log(tempSale/l.tempSale)`
**Stata code:**
```stata
xtset gvkey fyear
gen tempY = log(tempSale/l.tempSale)
```

**Issue:** Stata's `l.` operator is time-aware and returns null when there's a year gap. Python's `shift(1)` is position-based and incorrectly uses the wrong year's data.

**Checkpoint comparison for permno 79283:**
```
CHECKPOINT 2: After creating tempY and tempX
Year 1996:
  Stata tempY: -0.541934 (but later excluded from regression)
  Python tempY: -0.541934 (incorrectly calculated using 1994 data instead of missing 1995)
```

### Line 88: `asreg tempY tempXLag, window(fyear 8) min(6) by(gvkey)`
**Stata code:**
```stata
replace tempXLag = l`n'.tempX
asreg tempY tempXLag, window(fyear 8) min(6) by(gvkey)
rename _b_tempXLag gammaAbility`n'
```

**Issue:** Stata's asreg excludes observations where tempY was calculated across a year gap. Python includes all observations with non-null values.

**Checkpoint comparison for permno 79283, year 2001:**
```
CHECKPOINT 3: After asreg for lag 1
Stata gammaAbility1: -59.618244 (using 6 observations, excluding year 1996)
Python gammaAbility1: -51.266108 (using 7 observations, including invalid year 1996)

Data used in regression:
Stata: Years [1994, 1997, 1998, 1999, 2000, 2001] - 6 observations
Python: Years [1994, 1996, 1997, 1998, 1999, 2000, 2001] - 7 observations
```

### Line 101: `asrol tempNonZero, window(fyear 8) min(6) by(gvkey) stat(mean) gen(tempMean)`
**Stata code:**
```stata
replace tempNonZero = tempXLag >0 & !mi(tempXLag)
asrol tempNonZero, window(fyear 8) min(6) by(gvkey) stat(mean) gen(tempMean)
```

**Issue:** The tempMean calculation differs because Stata excludes year 1996 from the window.

**Checkpoint comparison for permno 79283:**
```
CHECKPOINT 4: After tempMean filtering for lag 1
Year 2001:
  Stata tempMean: 0.85714286 (6 out of 7, excluding year 1996)
  Python tempMean: 1.0 (7 out of 7, incorrectly including year 1996)

Year 2002:
  Stata tempMean: 0.85714286
  Python tempMean: 1.0
```

### Line 212: `egen RDAbility = rowmean(gammaAbil*)`
**Stata code:**
```stata
egen RDAbility = rowmean(gammaAbil*)
```

**Issue:** Since the gammaAbility values are different, the final RDAbility differs.

**Checkpoint comparison for permno 79283:**
```
CHECKPOINT 5: After rowmean of gammaAbil
Year 2001:
  Stata RDAbility: -59.61824 (based on correct gammaAbility1)
  Python RDAbility: -24.396323 (based on incorrect gammaAbility values)
```

## Summary of Checkpoint Deviations

| Checkpoint | Permno | Year | Variable | Stata Value | Python Value | Root Cause |
|------------|--------|------|----------|-------------|--------------|------------|
| CP3 | 79283 | 2001 | gammaAbility1 | -59.618244 | -51.266108 | Year 1996 included in Python |
| CP4 | 79283 | 2001 | tempMean | 0.857143 | 1.0 | Year 1996 excluded in Stata |
| CP5 | 79283 | 2001 | RDAbility | -59.61824 | -24.396323 | Cascading from CP3 |
| CP7 | 79283 | 2001 | Final RDAbility | -59.61824 | -24.396323 | Same issue |

## Next Steps
1. Implement gap detection in RDAbility.py
2. Test on permno 79283 to verify match with Stata
3. Apply similar fix to other predictors with lag issues
4. Update DocsForClaude/traps.md with this finding