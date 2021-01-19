* --------------
// DATA LOAD
use gvkey permno time_avail_m at ceq using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen tempAvAT = .5*(at + l12.at)
gen DelEqu = (ceq - l12.ceq)
replace DelEqu = DelEqu/tempAvAT
label var DelEqu "Change in common equity"
// SAVE
do "$pathCode/savepredictor" DelEqu