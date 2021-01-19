* --------------
// DATA LOAD
use gvkey permno time_avail_m lt using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(mve_c)
// SIGNAL CONSTRUCTION
gen Leverage = lt/mve_c
label var Leverage "Market leverage"
// SAVE
do "$pathCode/savepredictor" Leverage