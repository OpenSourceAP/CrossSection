* --------------
// DATA LOAD
use permno time_avail_m xrd using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge m:1 permno using "$pathDataIntermediate/IPODates", keep(master match) nogenerate keepusing(IPOdate)
// SIGNAL CONSTRUCTION
gen tempipo = (time_avail_m - IPOdate <= 36) & (time_avail_m - IPOdate > 6)
replace tempipo  = 0 if IPOdate == .
gen RDIPO = 0
replace RDIPO = 1 if tempipo  == 1 & xrd == 0
drop tempipo
label var RDIPO "IPO without R&D"
// SAVE
do "$pathCode/savepredictor" RDIPO