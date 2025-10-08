* ChNWC
* --------------

// DATA LOAD
use gvkey permno time_avail_m act che lct dlc at using "$pathDataIntermediate/m_aCompustat", clear

// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m

gen temp = ( (act - che) - (lct - dlc) )/at
gen ChNWC = temp - l12.temp

drop temp*
label var ChNWC "Change in Net Working Capital"

// SAVE
do "$pathCode/savepredictor" ChNWC