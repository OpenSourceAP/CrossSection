# Patent Data Investigation Notes

Date: 2025-06-27

## Issue Summary
PatentDataProcessed dataset follows a special pattern that requires further investigation and specialized handling.

## Key Findings

### Current Status
- Python script ZI_PatentCitations.py calls R script ZIR_Patents.R
- R script fails due to CRAN mirror configuration issues
- Fallback creates placeholder data with only 3 records vs Stata's 196,664 records
- Stata file: PatentDataProcessed.dta (6.00 MB, 196,664 rows, 4 columns)

### Data Structure
- Columns: gvkey, year, npat, ncitscale (all float64)
- Year range: 1976-2006
- 6,344 unique companies (gvkey)
- Identifiers: stock=gvkey (no time identifier listed in docs)

### Special Pattern Identified
This dataset appears to follow a different processing pattern:
1. Relies on external R script for data processing
2. R script likely processes raw patent citation data from external sources
3. Creates derived metrics (npat, ncitscale) from raw patent data
4. Not a simple CSV/database download like other datasets

### Action Required
- Fix R environment setup and CRAN mirror configuration
- Examine ZIR_Patents.R script logic to understand data processing
- Identify source patent data files or database connections
- May require different validation approach due to external data dependencies

### Recommendation
Defer this dataset to specialized fix session after completing other Type A pattern fixes, as it requires:
1. R environment debugging
2. Understanding of patent data sources
3. Potentially different validation methodology

## Related Files
- Code/DataDownloads/ZI_PatentCitations.do
- Code/DataDownloads/ZIR_Patents.R  
- pyCode/DataDownloads/ZI_PatentCitations.py
- Data/Intermediate/PatentDataProcessed.dta