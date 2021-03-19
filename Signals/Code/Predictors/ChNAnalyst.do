* ChNAnalyst
* --------------

// Prep IBES data
use "$pathDataIntermediate/IBES_EPS_Unadj", replace
keep if fpi == "1" 
keep if fpedats != . & fpedats > statpers + 30
keep tickerIBES time_avail_m numest statpers fpedats
save "$pathtemp/temp", replace


// DATA LOAD
use permno time_avail_m tickerIBES mve_c using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 tickerIBES time_avail_m using "$pathtemp/temp", keep(master match) nogenerate 

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen ChNAnalyst = 1 if numest < l3.numest & !mi(l3.numest)
replace ChNAnalyst = 0 if numest >= l3.numest & !mi(numest)
replace ChNAnalyst = . if time_avail_m >= ym(1987,7) & time_avail_m <= ym(1987,9) 

* only works in small firms (OP tab 2)
egen temp = fastxtile(mve_c), n(5)
keep if temp <= 2


// SAVE
label var ChNAnalyst "Decline in Analyst Coverage"
do "$pathCode/savepredictor" ChNAnalyst
