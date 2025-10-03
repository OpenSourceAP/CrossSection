* --------------
// DATA LOAD
use gvkey permno time_avail_m sale using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen sgr = (sale/l12.sale)-1
label var sgr "Annual sales growth"
// SAVE
do "$pathCode/saveplacebo" sgr