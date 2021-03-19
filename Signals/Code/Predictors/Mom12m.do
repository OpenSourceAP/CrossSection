* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear

// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
gen Mom12m = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)*(1+l6.ret)* ///
               (1+l7.ret)*(1+l8.ret)*(1+l9.ret)*(1+l10.ret)*(1+l11.ret) ) - 1
label var Mom12m "Twelve month momentum"

// SAVE
do "$pathCode/savepredictor" Mom12m