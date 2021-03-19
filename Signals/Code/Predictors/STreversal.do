* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
gen STreversal = ret
label var STreversal "Short-term reversal"
// SAVE
do "$pathCode/savepredictor" STreversal