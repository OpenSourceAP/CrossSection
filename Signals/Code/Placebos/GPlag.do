* --------------
// DATA LOAD
use gvkey permno time_avail_m sale cogs at using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen GPlag = (sale-cogs)/l12.at

label var GPlag "Gross profitability (lagged assets)"
// SAVE
do "$pathCode/saveplacebo" GPlag