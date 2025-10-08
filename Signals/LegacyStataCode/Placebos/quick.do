* --------------
// DATA LOAD
use gvkey permno time_avail_m act invt lct using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
gen quick = (act - invt)/lct
label var quick "Quick ratio"
// SAVE
do "$pathCode/saveplacebo" quick