* --------------
// Prep IBES data
use "$pathDataIntermediate/IBES_EPS_Unadj", replace
keep if fpi == "1" 
save "$pathtemp/temp", replace

// DATA LOAD
use permno time_avail_m tickerIBES using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 tickerIBES time_avail_m using "$pathtemp/temp", keep(master match) nogenerate keepusing(numest)

// SIGNAL CONSTRUCTION
gen nanalyst = numest
replace nanalyst = 0 if yofd(dofm(time_avail_m)) >=1989 & mi(nanalyst)
label var nanalyst "Number of analysts"

// SAVE
do "$pathCode/saveplacebo" nanalyst
