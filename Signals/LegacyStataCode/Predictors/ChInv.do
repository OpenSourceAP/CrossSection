* ChInv
* --------------

// DATA LOAD
use gvkey permno time_avail_m at invt using "$pathDataIntermediate/m_aCompustat", clear

// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m

gen ChInv 	=	(invt-l12.invt)/((at+l12.at)/2)

label var ChInv "Change in inventory"

// SAVE
do "$pathCode/savepredictor" ChInv