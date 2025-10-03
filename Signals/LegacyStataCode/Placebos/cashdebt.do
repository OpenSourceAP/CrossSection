* cashdebt
* --------------

// DATA LOAD
use gvkey permno time_avail_m ib dp lt using "$pathDataIntermediate/m_aCompustat", clear

// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m

gen cashdebt 	= (ib+dp)/((lt+l12.lt)/2)  // Cash flow to debt

label var cashdebt "Cash flow to debt"

// SAVE
do "$pathCode/saveplacebo" cashdebt