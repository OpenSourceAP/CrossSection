* --------------
// DATA LOAD
use gvkey permno time_avail_m ni ceq using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
gen RoE = ni/ceq 
label var RoE "Return on Equity"
// SAVE
do "$pathCode/savepredictor" RoE