* --------------
// DATA LOAD
use gvkey permno time_avail_m dp ppent using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen pchdepr = ((dp/ppent)-(l12.dp/l12.ppent))/(l12.dp/l12.ppent)
label var pchdepr "Change in depreciation to gross PPE"
// SAVE
do "$pathCode/saveplacebo" pchdepr