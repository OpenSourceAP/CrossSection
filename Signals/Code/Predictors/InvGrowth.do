* --------------
// DATA LOAD
use gvkey permno time_avail_m invt sic ppent at using "$pathDataIntermediate/m_aCompustat", clear
merge m:1 time_avail_m using "$pathDataIntermediate/GNPdefl", keep(match) nogenerate 

replace invt = invt/gnpdefl // op uses cpi

// Sample selection
drop if substr(sic,1,1) == "4"
drop if substr(sic,1,1) == "6"
drop if at <= 0 | ppent <= 0

// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen InvGrowth = invt/l12.invt - 1
label var InvGrowth "Inventory Growth"

// SAVE
do "$pathCode/savepredictor" InvGrowth

