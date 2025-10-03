* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear

// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
gen MomSeasonShort = l11.ret
label var MomSeasonShort "Return seasonality last year"

// SAVE
do "$pathCode/savepredictor" MomSeasonShort
