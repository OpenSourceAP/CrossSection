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
- **Current**: Data saved to `Data/Intermediate/` in DTA/CSV format
- **Target**: Python scripts should output to `Data/Intermediate/` in Parquet format
- **File naming**: Maintain same base names but with `.parquet` extension

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

### Python Environment
- Use `pandas` for data manipulation
- Use `pyarrow` for Parquet I/O  
- Use `wrds` library for database connections
- Use `pandas_datareader` for external data APIs
- Follow PEP 8 style guidelines

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
- Compare output files with original Stata results
- Validate row counts, column names, and summary statistics
- Test edge cases and missing data scenarios

## Project Status
Current progress tracked in individual Python files. Focus on replicating core WRDS data downloads first (A-K), then market data (O-W), before tackling specialized datasets (X-Z series).

## Commands
- **Run all downloads**: `python pyCode/01_DownloadData.py`
- **Test individual script**: `python pyCode/DataDownloads/[SCRIPT_NAME].py`
- **Check requirements**: `pip install -r pyCode/requirements.txt`