* --------------
// DATA LOAD
use gvkey permno time_avail_m sale rect using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
gen salerec = sale/rect
label var salerec "Sales to receivables"
// SAVE
do "$pathCode/saveplacebo" salerec