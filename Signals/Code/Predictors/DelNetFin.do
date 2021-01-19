* --------------
// DATA LOAD
use gvkey permno time_avail_m at pstk dltt dlc ivst ivao using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen tempAvAT = .5*(at + l12.at)
gen tempPSTK = pstk
replace tempPSTK = 0 if mi(pstk)
gen temp = (ivst + ivao) - (dltt + dlc + tempPSTK)  // Financial assets minus liabilities
gen DelNetFin = temp - l12.temp
replace DelNetFin = DelNetFin/tempAvAT
label var DelNetFin "Change in net financial assets"
// SAVE
do "$pathCode/savepredictor" DelNetFin