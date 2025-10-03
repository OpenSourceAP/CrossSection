* ChNCOA
* --------------

// DATA LOAD
use gvkey permno time_avail_m at act ivao using "$pathDataIntermediate/m_aCompustat", clear

// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m

gen temp = at - act - ivao
replace temp = at - act if mi(ivao)
gen ChNCOA = (temp - l12.temp)/l12.at
drop temp*

label var ChNCOA "Change in Noncurrent Operating Assets"

// SAVE
do "$pathCode/saveplacebo" ChNCOA