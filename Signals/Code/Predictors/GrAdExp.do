* --------------
// DATA LOAD
use permno time_avail_m at xad using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(master match) nogenerate keepusing(mve_c) 
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen GrAdExp = log(xad) - log(l12.xad)
egen tempSize = fastxtile(mve_c), n(10) by(time_avail)
replace GrAdExp = . if xad < .1 | tempSize == 1
label var GrAdExp "Growth in advertising expenses"
// SAVE
do "$pathCode/savepredictor" GrAdExp