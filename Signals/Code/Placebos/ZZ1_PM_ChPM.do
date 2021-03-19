* --------------
// DATA LOAD
use gvkey permno time_avail_m ni revt using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen PM = ni/revt
gen ChPM = PM - l12.PM
label var PM "Profit Margin"
label var ChPM "Change in Profit Margin"

// SAVE
do "$pathCode/saveplacebo" PM
do "$pathCode/saveplacebo" ChPM