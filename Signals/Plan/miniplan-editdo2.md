# Miniplan: Add Debug Checkpoints to MomVol

## Overview
Add strategic checkpoints to MomVol.do and MomVol.py to debug precision failures by examining specific problematic observations identified in test results.

## Prerequisites
1. Run `python3 Predictors/MomVol.py` from pyCode/ directory
2. Run `python3 utils/test_predictors.py --predictors MomVol` 
3. Check `Logs/testout_predictors.md` "**Largest Differences**" section to identify bad permno-yyyymm combinations

## Task 1: Edit Code/Predictors/MomVol.do

### CHECKPOINT 1: After momentum calculation
**Location**: After line 18: `gen Mom6m = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)) - 1`

**Add after line 18**:
```stata
* CHECKPOINT 1: Debug momentum calculation for problematic observations
list permno time_avail_m ret l.ret l2.ret l3.ret l4.ret l5.ret Mom6m if permno == [PERMNO] & time_avail_m == tm([YYYY]m[M])
```

### CHECKPOINT 2: After momentum quantiles  
**Location**: After line 19: `egen catMom = fastxtile(Mom6m), by(time_avail_m) n(10)`

**Add after line 19**:
```stata
* CHECKPOINT 2: Debug momentum quantiles
list permno time_avail_m Mom6m catMom if permno == [PERMNO] & time_avail_m == tm([YYYY]m[M])
summarize Mom6m if time_avail_m == tm([YYYY]m[M]), detail
_pctile Mom6m if time_avail_m == tm([YYYY]m[M]), n(10)
display "Momentum decile cutoffs for " %tm time_avail_m ": " r(r1) " " r(r2) " " r(r3) " " r(r4) " " r(r5) " " r(r6) " " r(r7) " " r(r8) " " r(r9)
```

### CHECKPOINT 3: After volume rolling calculation
**Location**: After line 22: `bys permno (time_avail_m): asrol vol, gen(temp) window(time_avail_m 6) min(5) stat(mean)`

**Add after line 22**:
```stata
* CHECKPOINT 3: Debug volume rolling calculation
list permno time_avail_m vol temp if permno == [PERMNO] & time_avail_m == tm([YYYY]m[M])
```

### CHECKPOINT 4: After volume quantiles
**Location**: After line 23: `egen catVol = fastxtile(temp), by(time_avail_m) n(3)`

**Add after line 23**:
```stata
* CHECKPOINT 4: Debug volume quantiles  
list permno time_avail_m temp catVol if permno == [PERMNO] & time_avail_m == tm([YYYY]m[M])
summarize temp if time_avail_m == tm([YYYY]m[M]), detail
_pctile temp if time_avail_m == tm([YYYY]m[M]), n(3)
display "Volume tercile cutoffs for " %tm time_avail_m ": " r(r1) " " r(r2)
tabulate catVol if time_avail_m == tm([YYYY]m[M])
```

### CHECKPOINT 5: After final signal construction
**Location**: After line 25: `gen MomVol = catMom if catVol == 3 // keep high vol at only`

**Add after line 25**:
```stata
* CHECKPOINT 5: Debug final signal assignment
list permno time_avail_m catMom catVol MomVol if permno == [PERMNO] & time_avail_m == tm([YYYY]m[M])
count if catVol == 3 & time_avail_m == tm([YYYY]m[M])
count if !missing(MomVol) & time_avail_m == tm([YYYY]m[M])
```

### CHECKPOINT 6: After time filter
**Location**: After line 28: `bys permno (time_avail_m): replace MomVol = . if _n < 24`

**Add after line 28**:
```stata
* CHECKPOINT 6: Debug time filter  
list permno time_avail_m _n MomVol if permno == [PERMNO] & time_avail_m == tm([YYYY]m[M])
```

## Task 2: Edit pyCode/Predictors/MomVol.py

### CHECKPOINT 1: After momentum calculation
**Location**: After line 55 (after Mom6m calculation)

**Add after line 55**:
```python
# CHECKPOINT 1: Debug momentum calculation for problematic observations  
print("CHECKPOINT 1: Momentum calculation")
debug_obs = df.filter((pl.col("permno") == [PERMNO]) & (pl.col("time_avail_m") == [YYYYMM]))
if len(debug_obs) > 0:
    print(debug_obs.select(["permno", "time_avail_m", "ret", "l1_ret", "l2_ret", "l3_ret", "l4_ret", "l5_ret", "Mom6m"]))
```

### CHECKPOINT 2: After momentum quantiles
**Location**: After line 77 (after catMom calculation)

**Add after line 77**:
```python
# CHECKPOINT 2: Debug momentum quantiles
print("CHECKPOINT 2: Momentum quantiles")
debug_obs = df_pd[(df_pd["permno"] == [PERMNO]) & (df_pd["time_avail_m"] == [YYYYMM])]
if len(debug_obs) > 0:
    print(debug_obs[["permno", "time_avail_m", "Mom6m", "catMom"]])
time_subset = df_pd[df_pd["time_avail_m"] == [YYYYMM]]["Mom6m"].dropna()
if len(time_subset) > 0:
    print(f"Momentum stats for {[YYYYMM]}: {time_subset.describe()}")
    print(f"Momentum decile cutoffs: {np.percentile(time_subset, [10, 20, 30, 40, 50, 60, 70, 80, 90])}")
```

### CHECKPOINT 3: After volume rolling calculation  
**Location**: After line 74 (after asrol calculation)

**Add after line 74**:
```python
# CHECKPOINT 3: Debug volume rolling calculation
print("CHECKPOINT 3: Volume rolling calculation")
debug_obs = df_pd[(df_pd["permno"] == [PERMNO]) & (df_pd["time_avail_m"] == [YYYYMM])]
if len(debug_obs) > 0:
    print(debug_obs[["permno", "time_avail_m", "vol", "temp"]])
```

### CHECKPOINT 4: After volume quantiles
**Location**: After line 78 (after catVol calculation)

**Add after line 78**:
```python  
# CHECKPOINT 4: Debug volume quantiles
print("CHECKPOINT 4: Volume quantiles")
debug_obs = df_pd[(df_pd["permno"] == [PERMNO]) & (df_pd["time_avail_m"] == [YYYYMM])]
if len(debug_obs) > 0:
    print(debug_obs[["permno", "time_avail_m", "temp", "catVol"]])
time_subset = df_pd[df_pd["time_avail_m"] == [YYYYMM]]["temp"].dropna()
if len(time_subset) > 0:
    print(f"Volume stats for {[YYYYMM]}: {time_subset.describe()}")
    print(f"Volume tercile cutoffs: {np.percentile(time_subset, [33.33, 66.67])}")
    print(f"Volume tercile counts: {df_pd[df_pd['time_avail_m'] == [YYYYMM]]['catVol'].value_counts().sort_index()}")
```

### CHECKPOINT 5: After final signal construction
**Location**: After line 89 (after MomVol assignment) in the polars section

**Add after line 89**:
```python
# CHECKPOINT 5: Debug final signal assignment  
print("CHECKPOINT 5: Final signal assignment")
debug_obs = df.filter((pl.col("permno") == [PERMNO]) & (pl.col("time_avail_m") == [YYYYMM]))
if len(debug_obs) > 0:
    print(debug_obs.select(["permno", "time_avail_m", "catMom", "catVol", "MomVol"]))
high_vol_count = len(df.filter((pl.col("catVol") == 3) & (pl.col("time_avail_m") == [YYYYMM])))
non_missing_count = len(df.filter((pl.col("MomVol").is_not_null()) & (pl.col("time_avail_m") == [YYYYMM])))
print(f"High volume stocks (catVol==3): {high_vol_count}")
print(f"Non-missing MomVol: {non_missing_count}")
```

### CHECKPOINT 6: After time filter
**Location**: After line 102 (after obs_num filter)

**Add after line 102**:
```python
# CHECKPOINT 6: Debug time filter
print("CHECKPOINT 6: Time filter") 
debug_obs = df.filter((pl.col("permno") == [PERMNO]) & (pl.col("time_avail_m") == [YYYYMM]))
if len(debug_obs) > 0:
    print(debug_obs.select(["permno", "time_avail_m", "obs_num", "MomVol"]))
```

## Usage Instructions

1. **Before adding checkpoints**: Run the test to identify problematic permno-yyyymm combinations from `Logs/testout_predictors.md`

2. **Replace placeholders**: In both files, replace:
   - `[PERMNO]` with the actual problematic permno (e.g., `10051`)
   - `[YYYY]m[M]` with the actual date in Stata format (e.g., `2007m4`)  
   - `[YYYYMM]` with the actual date in YYYYMM format (e.g., `200704`)

3. **Run modified scripts**: Execute both the Stata .do file and Python .py file to capture debug output

4. **Compare outputs**: Analyze the checkpoint outputs to identify where the calculations diverge between Stata and Python

## Notes
- Focus on one problematic observation at a time for cleaner debugging
- The checkpoints target key calculation points: momentum calculation, quantile assignments, volume rolling calculation, and filters
- Pay special attention to fastxtile/quantile calculations as these are common sources of precision differences