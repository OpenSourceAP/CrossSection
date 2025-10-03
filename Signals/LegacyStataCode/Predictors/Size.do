* --------------
// DATA LOAD
use permno time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
// SIGNAL CONSTRUCTION
gen Size = log(mve_c)
label var Size "Size"
// SAVE
do "$pathCode/savepredictor" Size