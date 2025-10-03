* --------------
// DATA LOAD
use permno time_avail_m prc using "$pathDataIntermediate/SignalMasterTable", clear
// SIGNAL CONSTRUCTION
gen Price = log(abs(prc))
label var Price "Price"
// SAVE
do "$pathCode/savepredictor" Price