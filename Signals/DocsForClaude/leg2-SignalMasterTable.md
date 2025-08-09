# SignalMasterTable Leg

`Signals/Code/SignalMasterTable.do` is run in `02_CreatePredictors.do` and `03_CreatePlacebos.do`. But we should think about it as its own leg of the project. 

## Files and descriptions

Stata:
- `Signals/Code/SignalMasterTable.do` 
  - Makes `SignalMasterTable.dta`
- `Signals/Data/Intermediate/SignalMasterTable.dta` 
  - Indexed by (permno, time_avail_m)

Python:
- `pyCode/SignalMasterTable.py` tbc
  - Makes `SignalMasterTable.parquet`
- `pyData/Intermediate/SignalMasterTable.parquet` 
  - Indexed by (permno, time_avail_m)

Test script
- `pyCode/utils/test_signalmaster.py`: 

## Requirements

### Simple requirements:
1. Column names and order match exactly
2. Column types match exactly
3. Python indexes are a superset of Stata indexes
  - All observations in the dta should be in the parquet

### Precision requirements: 

Define:
- Common rows: rows with indexes that are in both Stata and Python
- Perfect rows: common rows with columns that have no deviations
- Imperfect rows: common rows that are not perfect rows

The precision requirements are:
4. Imperfect cells / total cells < 0.1%
5. Imperfect rows / total rows < 0.1% or...
