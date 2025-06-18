# CrossSection Signals - Python Translation Project

## Project Overview
This project aims to translate Stata code in `Code/DataDownloads/` to Python equivalents in `pyCode/DataDownloads/`, replicating the exact data processing pipeline while outputting to Parquet format instead of DTA/CSV.

## Data Pipeline Structure

### Input Sources
The DataDownloads scripts process data from:
- **WRDS databases**: Compustat (Annual/Quarterly), CRSP (Monthly/Daily), IBES
- **External APIs**: FRED (Federal Reserve Economic Data), Fama-French data
- **Preprocessed files** (optional): Located in `Data/Prep/`
  - `iclink.csv` - IBES-CRSP linking table
  - `OptionMetrics.csv` - Options data 
  - `tr_13f.csv` - Thomson Reuters 13F holdings
  - `corwin_schultz_spread.csv` - Bid-ask spread estimates

### Output Structure
- **Stata Output**: Data saved to `Data/Intermediate/` in DTA/CSV format
- **Python Output**: Data saved to `pyData/Intermediate/` in Parquet format
- **File naming**: Maintain same base names but with `.parquet` extension

## Directory Structure

```
Signals/
├── Code/                    # Original Stata code
│   ├── DataDownloads/      # Stata data download scripts
│   ├── Predictors/         # Stata predictor generation
│   └── Placebos/          # Stata placebo generation
├── Data/                   # Stata data files
│   ├── Intermediate/       # Processed data from Stata (.dta/.csv)
│   ├── Prep/              # Preprocessed inputs
│   └── temp/              # Temporary Stata files
├── pyCode/                 # Python equivalent code (WORKING DIRECTORY)
│   ├── .venv/              # Python virtual environment
│   ├── DataDownloads/      # Python data download scripts
│   ├── requirements.txt    # Python dependencies
│   ├── 01_DownloadData.py  # Main download orchestrator
│   └── test_datadownloads_comparison.py  # Testing script
├── pyData/                 # Python data files
│   ├── Intermediate/       # Processed data from Python (.parquet)
│   └── temp/              # Temporary Python files
├── Logs/                   # Processing logs
```

## DataDownloads Script Mapping

### Core WRDS Data (A-K)
- `A_CCMLinkingTable.do` → `A_CCMLinkingTable.py` - CRSP-Compustat linking
- `B_CompustatAnnual.do` → `B_CompustatAnnual.py` - Annual fundamentals  
- `C_CompustatQuarterly.do` → `C_CompustatQuarterly.py` - Quarterly fundamentals
- `D_CompustatPensions.do` → `D_CompustatPensions.py` - Pension data
- `E_CompustatBusinessSegments.do` → `E_CompustatBusinessSegments.py` - Segment data
- `F_CompustatCustomerSegments.do` → `F_CompustatCustomerSegments.py` - Customer data
- `G_CompustatShortInterest.do` → `G_CompustatShortInterest.py` - Short interest
- `H_CRSPDistributions.do` → `H_CRSPDistributions.py` - Distribution events
- `I_CRSPmonthly.do` → `I_CRSPmonthly.py` - Monthly stock data
- `I2_CRSPmonthlyraw.do` → `I2_CRSPmonthlyraw.py` - Raw monthly data
- `J_CRSPdaily.do` → `J_CRSPdaily.py` - Daily stock data
- `K_CRSPAcquisitions.do` → `K_CRSPAcquisitions.py` - M&A events

### IBES Data (L-N)  
- `L_IBES_EPS_Unadj.do` → `L_IBES_EPS_Unadj.py` - Unadjusted EPS estimates
- `L2_IBES_EPS_Adj.do` → `L2_IBES_EPS_Adj.py` - Adjusted EPS estimates
- `M_IBES_Recommendations.do` → `M_IBES_Recommendations.py` - Analyst recommendations
- `N_IBES_UnadjustedActuals.do` → `N_IBES_UnadjustedActuals.py` - Actual earnings

### Market Data (O-W)
- `O_Daily_Fama-French.do` → `O_Daily_Fama-French.py` - Daily FF factors
- `P_Monthly_Fama-French.do` → `P_Monthly_Fama-French.py` - Monthly FF factors  
- `Q_MarketReturns.do` → `Q_MarketReturns.py` - Market return indices
- `R_MonthlyLiquidityFactor.do` → `R_MonthlyLiquidityFactor.py` - Liquidity factor
- `S_QFactorModel.do` → `S_QFactorModel.py` - Q-factor model data
- `T_VIX.do` → `T_VIX.py` - VIX volatility index
- `U_GNPDeflator.do` → `U_GNPDeflator.py` - GNP price deflator
- `V_TBill3M.do` → `V_TBill3M.py` - 3-month Treasury bill rates
- `W_BrokerDealerLeverage.do` → `W_BrokerDealerLeverage.py` - Broker-dealer leverage

### Credit & Alternative Data (X-Z)
- `X_SPCreditRatings.do` → `X_SPCreditRatings.py` - S&P credit ratings
- `X2_CIQCreditRatings.do` → `X2_CIQCreditRatings.py` - Capital IQ ratings
- `ZA_IPODates.do` → `ZA_IPODates.py` - IPO dates from Ritter
- `ZB_PIN.do` → `ZB_PIN.py` - Probability of informed trading
- `ZC_GovernanceIndex.do` → `ZC_GovernanceIndex.py` - Corporate governance index
- `ZF_CRSPIBESLink.do` → `ZF_CRSPIBESLink.py` - CRSP-IBES linking
- `ZI_PatentCitations.do` → `ZI_PatentCitations.py` - Patent citation data
- `ZL_CRSPOPTIONMETRICS.do` → `ZL_CRSPOPTIONMETRICS.py` - CRSP-OptionMetrics link

## Implementation Guidelines

### Requirements
- Python code should follow the stata counterpart as closely as possible
- The python code should use the same data sources as the stata code
- Output is parquet
  - Not pkl

### Python Environment
- Use `pandas` for data manipulation
- Use `pyarrow` for Parquet I/O  
- Use `wrds` library for database connections
- Use `pandas_datareader` for external data APIs
- Follow PEP 8 style guidelines

### Python Code Quality Standards
**CRITICAL: All Python code must follow these formatting rules to avoid linting errors:**

#### **Line Length & Formatting**
- **Max line length: 88 characters** (Black standard, more flexible than 79)
- Break long lines using parentheses or backslashes:
```python
# Good - use parentheses for function calls
result = some_long_function_name(
    parameter1, parameter2, parameter3
)

# Good - break long strings
message = (
    "This is a very long message that needs to be "
    "broken across multiple lines"
)
```

#### **Import Management**
- **Remove unused imports** - Only import what you actually use
- **Import order**: Standard library → Third-party → Local imports
```python
# Standard library first
import os
from pathlib import Path

# Third-party libraries  
import pandas as pd
import numpy as np

# Local imports last
from .utils import helper_function
```

#### **Whitespace Rules**
- **No trailing whitespace** on any line
- **End files with single newline** character
- **2 blank lines** before function/class definitions
- **2 blank lines** after function/class definitions at module level

#### **String Formatting**
- **Use f-strings only when interpolating variables**:
```python
# Good - f-string with variables
name = "data"
message = f"Processing {name} file"

# Bad - f-string without variables
message = f"Processing complete"  # Should be: "Processing complete"
```

#### **Variable Usage**
- **No unused variables** - Remove or prefix with underscore:
```python
# Bad
df, meta = read_stata_file()  # meta unused

# Good
df, _ = read_stata_file()  # or remove meta entirely
```

#### **Function Documentation**
- **All functions need docstrings**:
```python
def process_data(df):
    """Process the input dataframe.
    
    Args:
        df: Input pandas DataFrame
        
    Returns:
        Processed DataFrame
    """
    return df
```

#### **Linting Commands**
Run these before committing code:
```bash
# Activate virtual environment
source .venv/bin/activate

# Check specific file
flake8 filename.py

# Check all Python files
flake8 .

# Auto-format code (if black is installed)
black filename.py
```

### Data Processing Standards
1. **Maintain data integrity**: Exact same filtering, cleaning, and transformations
2. **Preserve column names**: Keep original variable names from Stata
3. **Handle missing values**: Replicate Stata's missing value conventions
4. **Date formatting**: Ensure consistent date handling across files
5. **Data types**: Match Stata numeric precision where possible

### Error Handling
- Implement robust error handling for database connections
- Log processing times and success/failure status
- Create error flag system similar to Stata's `01_DownloadDataFlags`

### Testing Strategy
- Run `test_datadownloads_comparison.py` to compare output files with original Stata results
- Ensure that at least 95% of the data is exact match
- Fix inexact matches by making sure the py script follows every step of the stata script


## Project Status
Current progress tracked in individual Python files. Focus on replicating core WRDS data downloads first (A-K), then market data (O-W), before tackling specialized datasets (X-Z series).

## Commands

**IMPORTANT**: All Python commands must be run from the `pyCode/` directory.

```bash
# Navigate to working directory
cd pyCode/

# Activate virtual environment (required for all operations)
source .venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Run all downloads
python3 01_DownloadData.py

# Run individual DataDownloads script
python3 DataDownloads/[SCRIPT_NAME].py

# Test data comparison 
python3 test_datadownloads_comparison.py --list
```

## Python Development Environment

### Working Directory
- **All Python scripts must be executed from `pyCode/`**
- **Virtual environment is located at `pyCode/.venv/`**
- **Data paths are relative to `pyCode/` (e.g., `../pyData/Intermediate/`)**

### Environment Setup
```bash
# Initial setup (from pyCode/ directory)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### API Keys and External Data Sources
- **FRED API Key**: Required for Federal Reserve Economic Data scripts
  - Scripts requiring FRED API: `V_TBill3M.py`, `T_VIX.py`, `U_GNPDeflator.py`
  - Environment variable: `FRED_API_KEY`
  - Get free API key: https://fred.stlouisfed.org/docs/api/api_key.html
  - Set in `.env` file: `FRED_API_KEY = your_api_key_here`
- **WRDS Access**: Required for financial database scripts
  - Environment variables: `WRDS_USERNAME`, `WRDS_PASSWORD`
  - Set in `.env` file with your WRDS credentials

### Virtual Environment Management
- **Only one .venv folder**: Located in `pyCode/.venv/`
- **Always activate before running scripts**: `source .venv/bin/activate`
- **Install packages in venv**: `pip install package_name`