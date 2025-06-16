# This folder is intended to mimic ../Code/, but to use python instead of stata.

## Project Structure

The project structure relative to git root

```
CrossSection/                    (git root)
├── Signals/
│   ├── Code/                   (Stata scripts - original)
│   ├── Data/                   (intermediate data files - auto-created)
│   ├── Logs/                   (log files - auto-created)
│   └── pyCode/                 (Python equivalent - this folder)
│       ├── DataDownloads/      (Python data download scripts)
│       ├── Predictors/         (Python predictor scripts)
│       ├── Placebos/           (Python placebo scripts)
│       └── PrepScripts/        (Python preprocessing scripts)
```

**Path Notes:**
- Current location: `Signals/pyCode/` (2 levels down from git root)
- Data gets saved to: `../Data/` (relative to pyCode)
- This matches the Stata structure where `$pathDataIntermediate` points to `../Data/`

## ../Code/ Structure

The ../Code/ directory contains the following structure:

### Main Processing Files
- `01_DownloadData.do` - Main data download script
- `02_CreatePredictors.do` - Creates predictor variables
- `03_CreatePlacebos.do` - Creates placebo variables
- `04_OM_Splicer_2024.R` - OptionMetrics splicer in R
- `SignalMasterTable.do` - Master signal table creation
- `master.do` - Master execution script
- `settings.do` - Configuration settings
- `saveplacebo.do` - Saves placebo variables
- `savepredictor.do` - Saves predictor variables
- `ffind.ado` - Stata utility function

### DataDownloads/
Contains scripts for downloading data from various sources (26 files A-Z):
- Compustat data (Annual, Quarterly, Pensions, Business Segments, Customer Segments, Short Interest)
- CRSP data (Monthly, Daily, Distributions, Acquisitions)
- IBES data (EPS, Recommendations, Actuals)
- Market data (Fama-French factors, Market returns, Liquidity factors, VIX, etc.)
- Specialized datasets (Credit ratings, IPO dates, Patents, Options, etc.)

### Predictors/
Contains 138+ predictor variable scripts including:
- Accounting-based predictors (Accruals, Asset Growth, Book-to-Market, etc.)
- Market-based predictors (Beta, Momentum, Volatility, etc.)
- Analyst-based predictors (Recommendations, Forecasts, etc.)
- Firm characteristics (Size, Age, Liquidity, etc.)

### Placebos/
Contains 93+ placebo variable scripts that mirror the predictors structure for robustness testing.

### PrepScripts/
Contains preprocessing and utility scripts:
- OptionMetrics processing
- TAQ data processing
- SAS conversion scripts
- Shell scripts for batch processing
