* ChangeInRecommendation
* --------------

// DATA LOAD
use permno tickerIBES time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 tickerIBES time_avail_m using "$pathDataIntermediate/IBES_Recommendations", keep(master match) nogenerate keepusing(ChangeInRecommendation)

// SIGNAL CONSTRUCTION
keep if !mi(ChangeInRecommendation)

// SAVE
do "$pathCode/savepredictor" ChangeInRecommendation