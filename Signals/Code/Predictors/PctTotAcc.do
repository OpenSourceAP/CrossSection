* --------------
// DATA LOAD
use gvkey permno time_avail_m ni prstkcc sstk dvt oancf fincf ivncf using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
gen PctTotAcc = ( ni - (prstkcc - sstk + dvt + oancf + fincf + ivncf) )/abs(ni)
label var PctTotAcc "Percent Total PctTotAcc"
// SAVE
do "$pathCode/savepredictor" PctTotAcc