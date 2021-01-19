* ChNCOL
* --------------

// DATA LOAD
use gvkey permno time_avail_m lt dlc dltt at using "$pathDataIntermediate/m_aCompustat", clear

// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m

gen temp = lt - dlc - dltt
replace temp = lt - dlc if mi(dltt)
gen ChNCOL = (temp - l12.temp)/l12.at
drop temp*

label var ChNCOL "Change in Noncurrent Operating Liabilities"

// SAVE
do "$pathCode/saveplacebo" ChNCOL