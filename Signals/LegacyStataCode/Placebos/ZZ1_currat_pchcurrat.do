* currat, pchcurrat
* --------------

// DATA LOAD
use gvkey permno time_avail_m act che rect invt lct ap using "$pathDataIntermediate/m_aCompustat", clear

// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m

gen act2 = act
replace act2 	= 	che + rect + invt if act2 ==.
replace lct 	= 	ap if lct ==.
gen currat 		= 	act2/lct  

gen pchcurrat 		= 	(currat - l12.currat)/(l12.currat)
replace pchcurrat 	= 	0 if pchcurrat ==.

label var currat "Current ratio"
label var pchcurrat "Change in current ratio"

// SAVE
do "$pathCode/saveplacebo" currat
do "$pathCode/saveplacebo" pchcurrat