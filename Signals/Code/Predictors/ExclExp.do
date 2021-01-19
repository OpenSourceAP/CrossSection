* --------------
// DATA LOAD
use permno gvkey time_avail_m tickerIBES using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(epspiq) nogenerate keep(match)
merge m:1 tickerIBES time_avail_m using "$pathDataIntermediate/IBES_UnadjustedActuals", keep(master match) nogenerate keepusing(int0a)
// SIGNAL CONSTRUCTION
gen ExclExp = int0a - epspiq
winsor2 ExclExp, replace cut(1 99) trim
label var ExclExp "Excluded Expenses"
// SAVE
do "$pathCode/savepredictor" ExclExp