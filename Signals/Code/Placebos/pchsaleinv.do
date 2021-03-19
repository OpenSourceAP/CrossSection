* --------------
// DATA LOAD
use gvkey permno time_avail_m sale invt using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen pchsaleinv = ( (sale/invt)-(l12.sale/l12.invt) ) / (l12.sale/l12.invt)
label var pchsaleinv "Change in sales to inventory"
// SAVE
do "$pathCode/saveplacebo" pchsaleinv