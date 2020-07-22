** This file puts all data together in one dataset
timer clear
timer on 1

// Start with monthly version of Compustat annual file
u "$pathProject/DataClean/m_aCompustat", clear

// Add monthly CRSP file
rename lpermno permno
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathProject/DataClean/m_CRSP", keep(using match) nogenerate  // Keep using data here because can compute return-based anomalies 
                                                        										   // regardless of availability of fundamentals + for longer time period
// Merge earnings announcement returns
merge 1:1 permno time_avail_m using "$pathProject/DataClean/AnnouncementReturns", keep(master match) nogenerate
																  
// Screen on Stock market information: common stocks and major exchanges 
keep if (shrcd == 10 | shrcd == 11 | shrcd == 12) & (exchcd == 1 | exchcd == 2 | exchcd == 3)

// Add gvkey based data:

// Compustat Pensions
gen year = year(dofm(time_avail_m))

preserve
	keep if gvkey == .
	save temp, replace  // Temporarily store obs with missing gvkeys in another file
restore
drop if gvkey ==.

merge m:1 gvkey year using "$pathProject/DataClean/CompustatPensions", keep(master match) nogenerate

// Credit Ratings and short interest
merge 1:1 gvkey time_avail_m using "$pathProject/DataClean/m_SP_creditratings", keep(master match) nogenerate
merge 1:1 gvkey time_avail_m using "$pathProject/DataClean/m_ShortInterest", keep(master match) nogenerate

// conglomerate returns
merge 1:1 gvkey time_avail_m using "$pathProject/DataClean/ConglomerateReturns", keep(master match) nogenerate

// monthly version of quarterly Compustat
merge 1:1 gvkey time_avail_m using "$pathProject/DataClean/m_QCompustat", keep(master match) nogenerate

// patent citation dataset
merge m:1 gvkey year using "$pathProject/DataClean/PatentDataProcessed", keep(master match) nogenerate

// Customer and Supplier Momentum
merge 1:1 gvkey time_avail_m using "$pathProject/DataClean/InputOutputMomentum", keep(master match) nogenerate

* Append obs without gvkey again
append using temp

// Add Consumer Price Index
merge m:1 time_avail_ using "$pathProject/DataClean/CPI", keep(master match) nogenerate

// Add GNP deflator
merge m:1 time_avail_ using "$pathProject/DataClean/GNPdefl", keep(master match) nogenerate

// Add CRSP Acquisition Dates
merge m:1 permno using "$pathProject/DataClean/m_CRSPAcquisitions", keep(master match) nogenerate

// Add Corwin's bid-ask spreads
merge 1:1 permno time_avail_m using "$pathProject/DataClean/BAspreadsCorwin", keep(master match) nogenerate 

// Add IPO dates
merge m:1 permno using "$pathProject/DataClean/IPODatesV2", keep(master match) nogenerate
gen IPO = (IPOdate == time_avail_m)

// Add monthly measures from daily CRSP
*merge 1:1 permno time_avail_m using "$pathProject/DataClean/m_BetaEtAl", keep(master match) nogenerate
merge 1:1 permno time_avail_m using "$pathProject/DataClean/m_DCRSP", keep(master match) nogenerate

// Add 13F data
merge 1:1 permno time_avail_m using "$pathProject/DataClean/TR_13F", keep(master match) nogenerate

// Add monthly tail risk for tail risk beta regressions
merge m:1 time_avail_m using "$pathProject/DataClean/TailRisk", keep(master match) nogenerate

// Merge Probability of Informed Trading data
merge m:1 permno year using "$pathProject/DataClean/aInformedTrading", keep(master match) nogenerate

// Broker-Dealer Leverage Beta
gen qtr = quarter(dofm(time_avail_m))
merge m:1 permno year qtr using "$pathProject/DataClean/BDLeverageBeta", keep(master match) nogenerate

// Customer momentum
merge 1:1 permno time_avail_m using "$pathProject/DataClean/customerMom", keep(master match) nogenerate

// Trading cost based on TAQ
merge 1:1 permno time_avail_m using "$pathProject/DataClean/tcost_TAQ", keep(master match) nogenerate

// Add Sin Stock classification from original paper and from segment file
merge m:1 permno using "$pathProject/DataClean/SinStocksHong", keep(master match) nogenerate
gen sinOrig = year >= begy & year <= endy & !mi(begy) & !mi(endy)
drop begy endy

merge m:1 gvkey using "$pathProject/DataClean/sinStocksAlgo", keep(master match)
gen sinAlgo = _merge == 3
drop _merge

// Add ticker-based data (many to one match due to permno-ticker not unique in crsp)
preserve
	keep if mi(ticker)
	save temp, replace
restore

drop if mi(ticker)

// Gompers et al Governance index
merge m:1 ticker time_avail_m using "$pathProject/DataClean/GovIndex", keep(master match) nogenerate

// Add OptionMetrics data
merge m:1 ticker time_avail_m using "$pathProject/DataClean/OptionMetrics", keep(master match) nogenerate
append using temp

// Add monthly IBES data
merge m:1 permno using "$pathProject/DataClean/IBESCRSPLinkingTable", keep(master match) nogenerate
merge m:1 tickerIBES time_avail_m using "$pathProject/DataClean/IBES_EPS", keep(master match) nogenerate
merge m:1 tickerIBES time_avail_m using "$pathProject/DataClean/IBES_EPSLongRun", keep(master match) nogenerate
merge m:1 tickerIBES time_avail_m using "$pathProject/DataClean/IBES_Recommendations", keep(master match) nogenerate
merge m:1 tickerIBES time_avail_m using "$pathProject/DataClean/IBES_UnadjustedActuals", keep(master match) nogenerate

// SAVE
compress
save "$pathProject/DataClean/m_MergedData", replace

***************************************************************************
erase temp.dta

timer off 1
timer list 1
