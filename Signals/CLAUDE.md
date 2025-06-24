# CrossSection Signals - Python Translation Project

## Project Overview
This project aims to translate Stata code in `Code/` to Python equivalents in `pyCode/`, replicating the exact data processing pipeline while outputting to Parquet format instead of DTA/CSV.

# Project Structure 

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
| Stata Script | Python Script | Output File | File Size | Description |
|-------------|---------------|-------------|-----------|-------------|
| `A_CCMLinkingTable.do` | `A_CCMLinkingTable.py` | CCMLinkingTable.dta | 2.7M | CRSP-Compustat linking |
| `B_CompustatAnnual.do` | `B_CompustatAnnual.py` | m_aCompustat.dta | 3.1G | Annual fundamentals |
| `C_CompustatQuarterly.do` | `C_CompustatQuarterly.py` | m_QCompustat.dta | 2.5G | Quarterly fundamentals |
| `D_CompustatPensions.do` | `D_CompustatPensions.py` | CompustatPensions.dta | 10M | Pension data |
| `E_CompustatBusinessSegments.do` | `E_CompustatBusinessSegments.py` | CompustatSegments.dta | 388M | Segment data |
| `F_CompustatCustomerSegments.do` | `F_CompustatCustomerSegments.py` | customerMom.dta | 4.1M | Customer data |
| `G_CompustatShortInterest.do` | `G_CompustatShortInterest.py` | monthlyShortInterest.dta | 49M | Short interest |
| `H_CRSPDistributions.do` | `H_CRSPDistributions.py` | CRSPdistributions.dta | 65M | Distribution events |
| `I_CRSPmonthly.do` | `I_CRSPmonthly.py` | monthlyCRSP.dta | 418M | Monthly stock data |
| `I2_CRSPmonthlyraw.do` | `I2_CRSPmonthlyraw.py` | monthlyCRSPraw.dta | 418M | Raw monthly data |
| `J_CRSPdaily.do` | `J_CRSPdaily.py` | dailyCRSP.dta | 3.8G | Daily stock data |
| `K_CRSPAcquisitions.do` | `K_CRSPAcquisitions.py` | m_CRSPAcquisitions.dta | 29K | M&A events |

### IBES Data (L-N)
| Stata Script | Python Script | Output File | File Size | Description |
|-------------|---------------|-------------|-----------|-------------|
| `L_IBES_EPS_Unadj.do` | `L_IBES_EPS_Unadj.py` | IBES_EPS_Unadj.dta | 284M | Unadjusted EPS estimates |
| `L2_IBES_EPS_Adj.do` | `L2_IBES_EPS_Adj.py` | IBES_EPS_Adj.dta | 919M | Adjusted EPS estimates |
| `M_IBES_Recommendations.do` | `M_IBES_Recommendations.py` | IBES_Recommendations.dta | 54M | Analyst recommendations |
| `N_IBES_UnadjustedActuals.do` | `N_IBES_UnadjustedActuals.py` | IBES_UnadjustedActuals.dta | 321M | Actual earnings |

### Market Data (O-W)
| Stata Script | Python Script | Output File | File Size | Description |
|-------------|---------------|-------------|-----------|-------------|
| `O_Daily_Fama-French.do` | `O_Daily_Fama-French.py` | dailyFF.dta | 1.0M | Daily FF factors |
| `P_Monthly_Fama-French.do` | `P_Monthly_Fama-French.py` | monthlyFF.dta | 53K | Monthly FF factors |
| `Q_MarketReturns.do` | `Q_MarketReturns.py` | monthlyMarket.dta | 33K | Market return indices |
| `R_MonthlyLiquidityFactor.do` | `R_MonthlyLiquidityFactor.py` | monthlyLiquidity.dta | 9.1K | Liquidity factor |
| `S_QFactorModel.do` | `S_QFactorModel.py` | d_qfactor.dta | 317K | Q-factor model data |
| `T_VIX.do` | `T_VIX.py` | d_vix.dta | 104K | VIX volatility index |
| `U_GNPDeflator.do` | `U_GNPDeflator.py` | GNPdefl.dta | 7.3K | GNP price deflator |
| `V_TBill3M.do` | `V_TBill3M.py` | TBill3M.dta | 4.9K | 3-month Treasury bill rates |
| `W_BrokerDealerLeverage.do` | `W_BrokerDealerLeverage.py` | brokerLev.dta | 4.0K | Broker-dealer leverage |

### Credit & Alternative Data (X-Z)
| Stata Script | Python Script | Output File | File Size | Description |
|-------------|---------------|-------------|-----------|-------------|
| `X_SPCreditRatings.do` | `X_SPCreditRatings.py` | m_SP_creditratings.dta | 20M | S&P credit ratings |
| `X2_CIQCreditRatings.do` | `X2_CIQCreditRatings.py` | m_CIQ_creditratings.dta | 17M | Capital IQ ratings |
| `ZA_IPODates.do` | `ZA_IPODates.py` | - | - | IPO dates from Ritter |
| `ZB_PIN.do` | `ZB_PIN.py` | pin_monthly.dta | 7.5M | Probability of informed trading |
| `ZC_GovernanceIndex.do` | `ZC_GovernanceIndex.py` | GovIndex.dta | 3.9M | Corporate governance index |
| `ZD_CorwinSchultz.do` | `ZD_CorwinSchultz.py` | BAspreadsCorwin.dta | 43M | Corwin-Schultz bid-ask spreads |
| `ZE_13F.do` | `ZE_13F.py` | TR_13F.dta | 52M | Thomson Reuters 13F holdings |
| `ZF_CRSPIBESLink.do` | `ZF_CRSPIBESLink.py` | IBESCRSPLinkingTable.dta | 213K | CRSP-IBES linking |
| `ZG_BidaskTAQ.do` | `ZG_BidaskTAQ.py` | hf_spread.dta | 31M | High-frequency bid-ask spreads |
| `ZH_OptionMetrics.do` | `ZH_OptionMetrics.py` | OptionMetricsBH.dta | 68M | OptionMetrics Black-Scholes data |
| `ZI_PatentCitations.do` | `ZI_PatentCitations.py` | PatentDataProcessed.dta | 6.0M | Patent citation data |
| `ZJ_InputOutputMomentum.do` | `ZJ_InputOutputMomentum.py` | InputOutputMomentum.dta | 270M | Input-output momentum |
| `ZK_CustomerMomentum.do` | `ZK_CustomerMomentum.py` | customerMom.dta | 4.1M | Customer momentum |
| `ZL_CRSPOPTIONMETRICS.do` | `ZL_CRSPOPTIONMETRICS.py` | OPTIONMETRICSCRSPLinkingTable.dta | 234K | CRSP-OptionMetrics link |

# Requirements

## Basic Requirements
- Python code should follow the stata counterpart as closely as possible
- The python code should use the same data sources as the stata code
- Output is parquet
  - Not pkl

## Python Environment
- Use `pandas` for data manipulation
- Use `pyarrow` for Parquet I/O  
- Use `wrds` library for database connections
- Use `pandas_datareader` for external data APIs
- Follow PEP 8 style guidelines


## Data Processing Standards
1. **Maintain data integrity**: Exact same filtering, cleaning, and transformations
2. **Preserve column names**: Keep original variable names from Stata
3. **Handle missing values**: Replicate Stata's missing value conventions
4. **Date formatting**: Ensure consistent date handling across files
5. **Data types**: Match Stata numeric precision where possible

## Error Handling
- Implement robust error handling for database connections
- Log processing times and success/failure status
- Create error flag system similar to Stata's `01_DownloadDataFlags`

## Paths

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
- Before running any python script, `source .venv/bin/activate`

### Environment Setup
```bash
# Initial setup (from pyCode/ directory)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Virtual Environment Management
- **Only one .venv folder**: Located in `pyCode/.venv/`
- **Always activate before running scripts**: `source .venv/bin/activate`
- **Install packages in venv**: `pip install package_name`

# Style Guidelines

## Python Code Quality Standards
**CRITICAL: All Python code must follow these formatting rules to avoid linting errors:**

### **Line Length & Formatting**
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

### **Import Management**
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

### **Whitespace Rules**
- **No trailing whitespace** on any line
- **End files with single newline** character
- **2 blank lines** before function/class definitions
- **2 blank lines** after function/class definitions at module level

### **String Formatting**
- **Use f-strings only when interpolating variables**:
```python
# Good - f-string with variables
name = "data"
message = f"Processing {name} file"

# Bad - f-string without variables
message = f"Processing complete"  # Should be: "Processing complete"
```

### **Variable Usage**
- **No unused variables** - Remove or prefix with underscore:
```python
# Bad
df, meta = read_stata_file()  # meta unused

# Good
df, _ = read_stata_file()  # or remove meta entirely
```

### **Function Documentation**
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

### **Linting Commands**
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