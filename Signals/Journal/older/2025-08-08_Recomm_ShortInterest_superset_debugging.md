# Recomm_ShortInterest Superset Debugging - August 8, 2025

## Problem Statement
Recomm_ShortInterest predictor failing superset test with Python missing 22,055-30,254 Stata observations (63.71% - 87.39% failure rate).

## Investigation Process

### Step 1: Target Observation Analysis
Selected specific missing observation: **permno=10051, yyyymm=200704** (Recomm_ShortInterest=1 in Stata)

**Data Availability Check:**
- ✅ SignalMasterTable: permno=10051, yyyymm=200704 exists (gvkey=16456, tickerIBES='HGR')
- ✅ monthlyCRSP: permno=10051, yyyymm=200704 exists (shrout=22.161)  
- ✅ monthlyShortInterest: gvkey=16456, yyyymm=200704 exists (shortint=14039.0)
- ❌ **Missing:** HGR recommendations in 200704

### Step 2: IBES Recommendations Analysis
**HGR Recommendation Pattern (2006-2008):**
- 200605: amaskcd=112695, ireccd=3
- 200606: amaskcd=57577, ireccd=2  
- 200701: amaskcd=57452, ireccd=2
- 200702: amaskcd=57577, ireccd=3
- **200704: NO DIRECT RECOMMENDATION** ❌
- 200706: amaskcd=41379, ireccd=2
- 200708: amaskcd=57577, ireccd=2

**Key Finding:** HGR has NO direct recommendation in 200704, but analyst 57577 has recommendations in 200702 and 200708. The rolling window should propagate the 200702 value (ireccd=3) to 200704.

### Step 3: Root Cause Identification

**Issue:** Python's tsfill implementation was incorrect

**Original Logic (WRONG):**
```python
# Creates time grid from ALL possible time_avail_m values in entire database
time_range = ibes_recs.select(["time_avail_m"]).unique().sort("time_avail_m")
```
- This created global time range from 199212 to 202505
- For each tempID, filled EVERY month in that range  
- **Result:** 59.4 million observations (70x expansion from 838K)
- **Consequence:** Process timeouts, no meaningful results

**Stata tsfill Behavior:**
- `tsfill` only fills missing periods within each panel's existing range
- Creates balanced panel for time-series operations
- Enables `asrol` to look back exactly 12 periods with correct time alignment

### Step 4: Attempted Solutions

**Solution 1: Fixed tsfill range (FAILED)**
```python
# Only fill months within each tempID's actual range
time_list = list(range(min_time, max_time + 1))
```
- **Result:** 59.4M observations, 70x expansion, timeouts
- **Problem:** Some tempIDs span 266+ years, unrealistic

**Solution 2: Conservative tsfill (FAILED)**  
```python
# Only fill months that exist in SignalMasterTable
relevant_times = valid_times.filter((pl.col("time_avail_m") >= min_time) & (pl.col("time_avail_m") <= max_time))
```
- **Result:** 7.3M observations, still too large
- **Problem:** Schema errors, complexity

**Solution 3: No tsfill (CURRENT BASELINE)**
```python
# Use original data without tsfill expansion
ibes_filled = ibes_recs.sort(["tempID", "time_avail_m"])
```
- **Result:** 14,630 observations vs 34,619 Stata (87.39% missing)
- **Problem:** Rolling window can't propagate across time gaps

### Step 5: Rolling Window Analysis

**Current Python Implementation:**
```python
pl.coalesce([
    pl.col("ireccd"),  # Current value
    pl.col("ireccd").shift(1).over("tempID"),  # 1 period back
    pl.col("ireccd").shift(2).over("tempID"),  # 2 periods back  
    # ... up to shift(11)
]).alias("ireccd12")
```

**Verification for HGR_57577:**
- 200702: ireccd=3 → ireccd12=3 ✅
- 200704: ireccd=null → ireccd12=3 ✅ (from shift(1) picking up 200702)
- 200708: ireccd=2 → ireccd12=2 ✅

**Conclusion:** Rolling window logic is CORRECT when data exists

## Key Insights

### 1. Translation Philosophy Lessons
- **NEVER create global time ranges** - always scope to specific needs
- **Understand data expansion implications** - 70x expansion indicates wrong approach  
- **tsfill is more nuanced** than simple range filling - only fills necessary gaps
- **Focus on core logic first** before optimizing data structures

### 2. Debugging Strategy Success
- **Bisection worked:** Traced single observation through entire pipeline
- **Data availability checking:** Confirmed all upstream data exists
- **Rolling window verification:** Confirmed forward-filling logic is correct

### 3. Root Cause Priority
1. **Primary:** Incorrect tsfill creating unusable data volume
2. **Secondary:** Missing rolling window propagation across time gaps
3. **Not the issue:** asrol stat(first) logic, quintile calculations, data type mismatches

## Current Status

**Baseline Performance:**
- Python: 14,630 observations
- Stata: 34,619 observations  
- Missing: 30,254 observations (87.39% superset failure)
- **Precision:** 100% accurate on common observations (0% differences)

**Target observation (permno=10051, yyyymm=200704):** Still missing from final result

## Recommended Next Steps

1. **Research Stata tsfill behavior** - understand exactly what time periods it fills
2. **Implement minimal tsfill** - only fill gaps needed for 12-month rolling windows
3. **Consider alternative approaches:**
   - Fill only months that will appear in final SignalMasterTable merge
   - Use time-based rolling windows instead of observation-based
   - Pre-filter tempIDs to reasonable time ranges

4. **Performance constraints:** Any solution must complete in <2 minutes
5. **Data expansion limit:** Maximum ~2-3x expansion from original 838K observations

## Technical Lessons

- **Polars group_by iteration** can be memory intensive for large datasets
- **Time-based operations** require careful data expansion analysis
- **Rolling window logic** is correct but requires proper time filling
- **Schema consistency** critical when joining multiple data transformations

## Success Metrics
- [ ] Superset test >95% (missing <5% of Stata observations)  
- [ ] Processing time <2 minutes
- [ ] Data expansion <3x original size
- [ ] Target observation (permno=10051, yyyymm=200704) appears in final result

---
*Session completed: Identified root cause, tested multiple solutions, established baseline performance. Ready for next iteration.*