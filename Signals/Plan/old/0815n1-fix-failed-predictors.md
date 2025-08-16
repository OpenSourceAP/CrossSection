# Plan: Fix Failed Predictor Scripts

Aug 15: 9 predictor scripts failed during execution with 3 distinct error types.

## Problem Summary

From `Logs/02_CreatePredictors_console.txt`, these scripts failed:
- **ModuleNotFoundError** (4 scripts): MomOffSeason.py, MomOffSeason06YrPlus.py, MomOffSeason11YrPlus.py, MomOffSeason16YrPlus.py
- **SchemaError** (3 scripts): RDAbility.py, Recomm_ShortInterest.py, TrendFactor.py  
- **ValueError** (2 scripts): VarCF.py, ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py

## Root Causes & Solutions

### 1. Import Path Issue (4 scripts)
**Problem**: `from utils.asrol import asrol` fails with "No module named 'utils'"
**Cause**: Scripts run from `pyCode/` but have `sys.path.append('..')` which doesn't resolve correctly
**Solution**: Fix import path to use absolute path resolution

### 2. Schema Type Errors (3 scripts)  
**Problem**: `SchemaError: invalid series dtype: expected Duration, got i16/i64`
**Cause**: Polars expects Duration type but gets integer for time columns
**Solution**: Add proper type casting in the scripts

### 3. Missing 'sd' Statistic (2 scripts)
**Problem**: `ValueError: Unsupported statistic: sd`
**Cause**: asrol.py supports 'std' but not 'sd' alias
**Solution**: Add 'sd' -> 'std' mapping in utils/asrol.py

## Task: Fix all failed predictor scripts

Work on scripts in order of error type (easiest fixes first).

## Progress Tracking

### Import Path Fixes (Priority 1)
- MomOffSeason.py
  - ❌ FAILED: ModuleNotFoundError: No module named 'utils'
- MomOffSeason06YrPlus.py  
  - ❌ FAILED: ModuleNotFoundError: No module named 'utils'
- MomOffSeason11YrPlus.py
  - ❌ FAILED: ModuleNotFoundError: No module named 'utils'
- MomOffSeason16YrPlus.py
  - ❌ FAILED: ModuleNotFoundError: No module named 'utils'

### Missing Statistic Fix (Priority 2)
- Add 'sd' alias to utils/asrol.py
  - ❌ NEEDS: Add 'sd': lambda col: col.rolling_std(...) mapping
- VarCF.py
  - ❌ FAILED: ValueError: Unsupported statistic: sd
- ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py
  - ❌ FAILED: ValueError: Unsupported statistic: sd

### Schema Type Fixes (Priority 3)
- RDAbility.py
  - ❌ FAILED: SchemaError: invalid series dtype: expected Duration, got i16 for 'fyear'
- Recomm_ShortInterest.py
  - ❌ FAILED: SchemaError: invalid series dtype: expected Duration, got i64 for 'time_avail_m'
- TrendFactor.py
  - ❌ FAILED: SchemaError: invalid series dtype: expected Duration, got i64 for 'time_temp'

## Next Steps
1. Fix import paths first (easiest)
2. Add 'sd' statistic support to asrol.py
3. Debug and fix schema type mismatches
4. Test all fixes by running 02_CreatePredictors.py