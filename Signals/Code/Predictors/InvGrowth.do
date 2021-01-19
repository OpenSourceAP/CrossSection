* --------------
// DATA LOAD
use gvkey permno time_avail_m invt using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen InvGrowth = l12.invt/l24.invt - 1
label var InvGrowth "Inventory Growth"
// SAVE
do "$pathCode/savepredictor" InvGrowth