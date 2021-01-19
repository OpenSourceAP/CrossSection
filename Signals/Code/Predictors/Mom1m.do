* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
gen Mom1m = ret
label var Mom1m "Short-term reversal"
// SAVE
do "$pathCode/savepredictor" Mom1m