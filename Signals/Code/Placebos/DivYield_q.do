* --------------
// DATA LOAD
use permno time_avail_m mve_c prc using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/mCRSPdistributions", keep(master match) nogenerate keepusing(divamt) 
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen temp = divamt
replace temp = 0 if divamt ==.
gen DivYield_q = (temp + l1.temp + l2.temp)/abs(prc)

egen tempsize = fastxtile(mve_c), by(time_avail_m) n(4)
replace DivYield_q = . if tempsize >= 3
// see table 1B
cap drop temp*
label var DivYield_q "Dividend Yield (quarterly)"
// SAVE
do "$pathCode/saveplacebo" DivYield_q