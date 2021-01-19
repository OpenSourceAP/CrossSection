* ChNAnalyst
* --------------

// DATA LOAD
use permno time_avail_m tickerIBES using "$pathDataIntermediate/SignalMasterTable", clear

merge m:1 tickerIBES time_avail_m using "$pathDataIntermediate/IBES_EPS", keep(master match) nogenerate keepusing(numest)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen ChNAnalyst = 1 if numest < l3.numest & !mi(l3.numest)
replace ChNAnalyst = 0 if numest >= l3.numest & !mi(numest)
replace ChNAnalyst = . if time_avail_m >= ym(1987,7) & time_avail_m <= ym(1987,9) 

label var ChNAnalyst "Decline in Analyst Coverage"

// SAVE
do "$pathCode/savepredictor" ChNAnalyst