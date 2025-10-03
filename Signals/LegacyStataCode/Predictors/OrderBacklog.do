* --------------
// DATA LOAD
use gvkey permno time_avail_m ob at using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen OrderBacklog = ob/(.5*(at + l12.at))
replace OrderBacklog = . if ob == 0
label var OrderBacklog "Order Backlog"
// SAVE
do "$pathCode/savepredictor" OrderBacklog