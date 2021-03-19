// PREP DISTRIBUTIONS DATA
use "$pathDataIntermediate/CRSPdistributions", clear

* collapse by exdt: this date tends to come first
gen time_avail_m = mofd(exdt)
format time_avail_m %tm
drop if time_avail_m == . | divamt == .

* sum dividends
gcollapse (sum) divamt, by(permno time_avail_m)

save "$pathtemp/tempdivamt", replace

* --------------
// DATA LOAD
use permno time_avail_m mve_c prc using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathtemp/tempdivamt", keep(master match) nogenerate keepusing(divamt) 

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
replace divamt = 0 if divamt ==.
asrol divamt, gen(divann) by(permno) stat(sum) window(time_avail_m 12) min(6) 
gen DivYieldAnn = divamt/abs(prc)


// see table 1B
label var DivYieldAnn "Dividend Yield (Past Year)"

// SAVE
do "$pathCode/saveplacebo" DivYieldAnn


