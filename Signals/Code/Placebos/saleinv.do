* --------------
// DATA LOAD
use gvkey permno time_avail_m sale invt using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
gen saleinv = sale/invt
label var saleinv "Sales to inventory"
// SAVE
do "$pathCode/saveplacebo" saleinv