# Input-Output Momentum Investigation Notes

Date: 2025-06-27

## Issue Summary
InputOutputMomentumProcessed dataset has complex algorithmic issues requiring specialized debugging beyond Type A pattern fixes.

## Key Findings

### Current Status
- Python script downloads BEA Input-Output data successfully
- Processes 61 years of historical data (1963-2023)
- Creates 269,673 I-O weight observations
- Fails during weighted average calculation with "Weights sum to zero" error
- Produces empty output (0 rows) vs Stata's 2,906,304 rows

### Technical Issues Identified

#### 1. Data Filtering Too Aggressive
- After CCM merge: 3,980,460 rows
- After industry mapping: 3,980,460 rows  
- After dropping NaN beaind: 1,875 rows (99.95% data loss!)
- Industry returns: 1,543 observations

#### 2. Weight Calculation Error
```
ZeroDivisionError: Weights sum to zero, can't be normalized
```
- Occurs in `np.average(x['retmatch'], weights=x['weight'])` call
- Suggests some industry groups have all zero weights
- May be due to self-industry weight removal or data gaps

#### 3. Data Structure Mismatch
- Expected: 2.9M rows spanning multiple years/months
- Current: Empty output after error
- Column structure matches but data generation fails

### Root Cause Analysis Required

#### Data Pipeline Issues
1. **Industry Mapping Logic**: NAICS to BEA industry mapping may be too restrictive
2. **Weight Calculation**: I-O table processing may not preserve non-zero weights properly
3. **Time Window Alignment**: Year availability vs data availability mismatch
4. **Data Type Handling**: Float precision issues in weight calculations

#### Algorithmic Complexity
1. **Complex Multi-Table Processing**: 
   - BEA Make/Use tables from 1963-2023
   - Compustat NAICS mapping
   - CRSP returns calculation
   - CCM linking across time

2. **Temporal Logic**: 
   - 5-year lag application
   - Monthly expansion logic
   - Forward-fill requirements

### Comparison with Stata Implementation
- Stata file: 110.87 MB, 2,906,304 rows
- Python produces: 0 rows due to algorithm failure
- Identifiers: gvkey (stock), time_avail_m (time)
- Expected data range: 1987+ (based on sample data)

## Action Required

### Immediate Next Steps
1. **Fix Weight Calculation**: Handle zero-weight cases in np.average calls
2. **Debug Industry Mapping**: Investigate 99.95% data loss after beaind filtering
3. **Validate I-O Processing**: Check BEA table parsing and weight extraction
4. **Compare with Stata Logic**: Examine original .do file for processing differences

### Long-term Investigation
1. **Algorithm Validation**: Reproduce Menzly-Ozbas methodology accurately
2. **Data Source Verification**: Ensure BEA URLs and data structure match expectations
3. **Performance Optimization**: Handle large dataset processing efficiently
4. **Integration Testing**: Validate end-to-end pipeline with known good data

## Recommendation
Defer this dataset to specialized debugging session requiring:
1. In-depth algorithm review and statistical methodology validation
2. BEA data structure analysis and parsing logic verification  
3. Multi-stage debugging of the complex processing pipeline
4. Potentially different validation approach due to algorithmic complexity

This is not a simple Type A pattern fix but requires algorithmic debugging and methodology validation.

## Related Files
- pyCode/DataDownloads/ZJ_InputOutputMomentum.py (533 lines of complex logic)
- Code/DataDownloads/ZJ_InputOutputMomentum.do (original Stata implementation)
- Data/Intermediate/InputOutputMomentumProcessed.dta (target output)