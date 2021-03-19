* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
gen IntMom = ( (1+l7.ret)*(1+l8.ret)*(1+l9.ret)*(1+l10.ret)*(1+l11.ret)*(1+l12.ret) ) - 1
label var IntMom "Intermediate Momentum"
// SAVE
do "$pathCode/savepredictor" IntMom