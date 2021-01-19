* --------------
// DATA LOAD
use gvkey permno time_avail_m ppegt invt at ppent using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen invest = ((ppegt-l12.ppegt) + (invt-l12.invt))/l12.at
replace invest = ((ppent-l12.ppent) +  (invt-l12.invt))/ l12.at if ppegt ==.
label var invest "Capex and inventory"
// SAVE
do "$pathCode/saveplacebo" invest