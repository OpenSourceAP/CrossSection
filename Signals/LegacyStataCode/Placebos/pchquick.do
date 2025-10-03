* --------------
// DATA LOAD
use gvkey permno time_avail_m act invt lct using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen pchquick = ( (act-invt)/lct - (l12.act-l12.invt)/l12.lct ) /  ((l12.act-l12.invt)/l12.lct)
replace pchquick = 0 if pchquick ==. & l12.pchquick ==.
label var pchquick "Change in quick ratio"
// SAVE
do "$pathCode/saveplacebo" pchquick