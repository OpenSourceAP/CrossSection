* --------------
// DATA LOAD
use gvkey permno time_avail_m sstk dv prstkc dltis dltr at using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
gen XFIN = (sstk - dv - prstkc + dltis - dltr)/at
label var XFIN "Net External Financing"
// SAVE
do "$pathCode/savepredictor" XFIN