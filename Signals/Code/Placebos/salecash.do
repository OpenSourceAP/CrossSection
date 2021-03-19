* --------------
// DATA LOAD
use gvkey permno time_avail_m sale che using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
gen salecash = sale/che 
label var salecash "Sales to cash"
// SAVE
do "$pathCode/saveplacebo" salecash