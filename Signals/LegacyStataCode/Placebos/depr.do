* --------------
// DATA LOAD
use gvkey permno time_avail_m dp ppent using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
gen depr = dp/ppent 
label var depr "Depreciation to PPE"
// SAVE
do "$pathCode/saveplacebo" depr