* --------------
// DATA LOAD
use gvkey permno time_avail_m sale cogs at using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen GP = (sale-cogs)/at

label var GP "Gross profitability"

// SAVE
do "$pathCode/savepredictor" GP