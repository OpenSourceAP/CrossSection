# Missing Python DataDownloads Scripts Implementation Plan

**Timestamp:** 2025-06-19  
**Status:** Planning Phase  
**Location:** CrossSection/Signals/pyCode/DataDownloads/

## Overview

Complete the Python translation project by implementing 7 missing DataDownloads scripts that correspond to existing Stata `.do` files. This will achieve 100% parity between `Code/DataDownloads/` and `pyCode/DataDownloads/`.

## Missing Scripts Analysis

### 1. FRED API Scripts (1 script)
**W_BrokerDealerLeverage.py**
- **Source:** FRED API
- **Stata file:** W_BrokerDealerLeverage.do
- **Output:** brokerLev.parquet
- **Implementation:** Use `pandas_datareader` with FRED API key
- **Size:** ~4.0K records

### 2. Data/Prep CSV Processing Scripts (3 scripts)
**ZD_CorwinSchultz.py**
- **Source:** `../Data/Prep/corwin_schultz_spread.csv` ✓ (exists)
- **Processing:** Parse month format, create time_avail_m, rename hlspread → BidAskSpread
- **Output:** BAspreadsCorwin.parquet (~43M)

**ZE_13F.py**
- **Source:** `../Data/Prep/tr_13f.csv` ✓ (exists)  
- **Processing:** Parse rdate, create time_avail_m, forward-fill missing months
- **Output:** TR_13F.parquet (~52M)

**ZG_BidaskTAQ.py**
- **Source:** `../Data/Prep/hf_monthly.csv` ✓ (exists)
- **Processing:** Parse yearm format, create hf_spread from espread_pct_mean
- **Output:** hf_spread.parquet (~31M)

### 3. OptionMetrics Processing Script (1 script)
**ZH_OptionMetrics.py**
- **Source:** `../Data/Prep/OptionMetrics*.csv` files ✓ (multiple files exist)
- **Processing:** Complex options data merging and calculations
- **Output:** OptionMetricsBH.parquet (~68M)

### 4. R-to-Python Conversion Scripts (2 scripts)
**ZI_PatentCitations.py**
- **Original:** ZIR_Patents.R + ZI_PatentCitations.do
- **Processing:** Patent citation data processing (R logic → Python)
- **Output:** PatentDataProcessed.parquet (~6.0M)

**ZJ_InputOutputMomentum.py**
- **Original:** ZJR_InputOutputMomentum.R + ZJ_InputOutputMomentum.do  
- **Processing:** Input-output momentum (R logic + Stata post-processing → Python)
- **Output:** InputOutputMomentumProcessed.parquet (~270M)

## Implementation Strategy

### Phase 1: CSV Processing Scripts (High Priority)
1. **ZD_CorwinSchultz.py** - Straightforward CSV processing
2. **ZE_13F.py** - CSV + forward-fill logic
3. **ZG_BidaskTAQ.py** - Simple CSV transformation

**Python Patterns:**
```python
# Standard CSV reading
data = pd.read_csv("../Data/Prep/filename.csv")

# Date parsing for time_avail_m
data['time_avail_m'] = pd.to_datetime(data['date_col']).dt.to_period('M')

# Forward-fill for missing months (ZE_13F)
data = data.set_index(['permno', 'time_avail_m']).fillna(method='ffill')

# Output to parquet
data.to_parquet("../pyData/Intermediate/filename.parquet")
```

### Phase 2: API Script (Medium Priority)  
4. **W_BrokerDealerLeverage.py** - FRED API implementation
   - Follow existing FRED patterns from V_TBill3M.py, T_VIX.py, U_GNPDeflator.py
   - Requires FRED_API_KEY environment variable

### Phase 3: Complex Processing (Lower Priority)
5. **ZH_OptionMetrics.py** - Multiple CSV file processing
6. **ZI_PatentCitations.py** - R logic conversion  
7. **ZJ_InputOutputMomentum.py** - R logic + Stata post-processing

### Phase 4: R Script Analysis
For R-to-Python conversions, analyze the R scripts to understand:
- Data sources and file formats
- Statistical calculations and transformations  
- Output data structures
- Integration points with Stata post-processing

## Success Criteria

1. **100% Script Parity:** All 7 missing Python scripts implemented
2. **Data Quality:** >95% exact match with Stata outputs using test_datadownloads_comparison.py
3. **Format Consistency:** All outputs in `.parquet` format in `pyData/Intermediate/`
4. **Code Quality:** Pass flake8 linting, follow existing patterns
5. **Documentation:** Each script includes docstrings and error handling

## Dependencies

### Environment Requirements
- Python virtual environment: `pyCode/.venv/`
- FRED API key for W_BrokerDealerLeverage.py
- All CSV files confirmed present in `Data/Prep/`

### Library Dependencies  
- pandas, pyarrow (existing)
- pandas_datareader (for FRED API)
- numpy (for numerical processing)

## Implementation Order

**Priority 1 (Quick Wins):**
1. ZD_CorwinSchultz.py
2. ZG_BidaskTAQ.py  
3. ZE_13F.py

**Priority 2 (Moderate Complexity):**
4. W_BrokerDealerLeverage.py
5. ZH_OptionMetrics.py

**Priority 3 (High Complexity):**
6. ZI_PatentCitations.py
7. ZJ_InputOutputMomentum.py

## Notes

- All scripts must be executed from `pyCode/` directory
- Virtual environment must be activated: `source .venv/bin/activate`  
- Test each script individually before integration
- Update `01_DownloadData.py` to include new scripts once completed
- Follow PKL→Parquet conversion lessons learned for exact data matching

## Next Steps

1. Start with ZD_CorwinSchultz.py (simplest CSV processing)
2. Test data comparison against Stata output
3. Iterate through remaining scripts by priority
4. Run comprehensive testing suite upon completion

---
*Plan created: 2025-06-19*  
*Project: CrossSection Signals Python Translation*