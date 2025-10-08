* --------------
// DATA LOAD
use gvkey permno time_avail_m capx revt using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen Investment = capx/revt 
bys permno: asrol Investment, gen(tempMean) window(time_avail_m 36) min(24) stat(mean)
replace Investment = Investment/tempMean
replace Investment = . if revt<10  // Replace with missing if revenue less than 10 million (units are millions)
drop temp*
label var Investment "Investment"
// SAVE
do "$pathCode/savepredictor" Investment