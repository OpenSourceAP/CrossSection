* --------------
// DATA LOAD
use gvkey permno time_avail_m sale cogs using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen pchgm_pchsale = (((sale-cogs)-(l12.sale-l12.cogs))/(l12.sale-l12.cogs))-((sale-l12.sale)/l12.sale)
label var pchgm_pchsale "Margin growth over sales growth"
// SAVE
do "$pathCode/saveplacebo" pchgm_pchsale