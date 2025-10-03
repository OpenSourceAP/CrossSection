* --------------
// DATA LOAD
use gvkey permno time_avail_m at pstk dltt dlc using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen tempAvAT = .5*(at + l12.at)
gen tempPSTK = pstk
replace tempPSTK = 0 if mi(pstk)
gen DelFINL = (dltt + dlc + tempPSTK) - (l12.dltt + l12.dlc + l12.tempPSTK)
replace DelFINL = DelFINL/tempAvAT
label var DelFINL "Change in financial liabilities"
// SAVE
do "$pathCode/savepredictor" DelFINL