* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
gen MomSeasAlt1a = l11.ret
label var MomSeasAlt1a "Return Seasonality (1 year)"
// SAVE
do "$pathCode/savepredictor" MomSeasAlt1a