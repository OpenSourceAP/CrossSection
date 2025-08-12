# sicff Function Usage in Stata Files

## Overview
The `sicff` function is used to generate Fama-French industry classifications from SIC codes in Stata.

## Files Using sicff in Code/Predictors/

Found 5 files that use the `sicff` function:

1. **EarnSupBig.do** (Line 36)
   - `sicff sicCRSP, generate(tempFF48) industry(48)`

2. **Frontier.do** (Line 15)  
   - `sicff sicCRSP, generate(tempFF48) industry(48)`

3. **IndRetBig.do** (Line 5)
   - `sicff sicCRSP, generate(tempFF48) industry(48)`

4. **ZZ1_OrgCap_OrgCapNoAdj.do** (Line 40)
   - `sicff sicCRSP, generate(tempFF17) industry(17)`

5. **sinAlgo.do** (Line 56)
   - `sicff sicCRSP, generate(tmpFF48) industry(48)`

## Usage Pattern
```stata
sicff sicCRSP, generate(tempFF##) industry(##)
```

Where:
- `sicCRSP`: Input SIC code variable
- `tempFF##`: Generated output variable name for industry classification
- `industry(##)`: Number of industries (17 or 48)

## Industry Classifications
- **FF48**: 48 industry classification (most common)
- **FF17**: 17 industry classification (used in OrgCap predictor)

## Python Translation Notes
When translating these files to Python, will need to implement equivalent Fama-French industry classification logic or use an existing Python library that provides sicff functionality.