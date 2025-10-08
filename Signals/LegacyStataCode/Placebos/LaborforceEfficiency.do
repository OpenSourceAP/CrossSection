* --------------
// DATA LOAD
use gvkey permno time_avail_m sale emp using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen temp = sale/emp
gen LaborforceEfficiency = (temp - l12.temp)/l12.temp
label var LaborforceEfficiency "Laborforce efficiency"
// SAVE
do "$pathCode/saveplacebo" LaborforceEfficiency