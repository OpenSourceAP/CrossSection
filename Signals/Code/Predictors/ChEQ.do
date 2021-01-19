* ChEQ
* --------------

// DATA LOAD
use gvkey permno time_avail_m ceq using "$pathDataIntermediate/m_aCompustat", clear

// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m

gen ChEQ = ceq/l12.ceq if ceq >0 & l12.ceq >0

label var ChEQ "Sustainable Growth"

// SAVE
do "$pathCode/savepredictor" ChEQ