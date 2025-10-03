* ChNNCOA
* --------------

// DATA LOAD
use gvkey permno time_avail_m at act ivao lt dlc dltt using "$pathDataIntermediate/m_aCompustat", clear

// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m

gen temp = ( (at - act - ivao)  - (lt - dlc - dltt) )/at
gen ChNNCOA = temp - l12.temp

drop temp*
label var ChNNCOA "Change in Net Noncurrent Operating Assets"

// SAVE
do "$pathCode/savepredictor" ChNNCOA