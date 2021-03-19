* CapTurnover
* --------------

// DATA LOAD
use gvkey permno time_avail_m sale at using "$pathDataIntermediate/m_aCompustat", clear

// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m

gen CapTurnover = l12.sale/l24.at

label var CapTurnover "Capital turnover"

// SAVE
do "$pathCode/saveplacebo" CapTurnover