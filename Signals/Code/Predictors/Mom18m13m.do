* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
gen Mom18m13m = ( (1+l13.ret)*(1+l14.ret)*(1+l15.ret)*(1+l16.ret)*(1+l17.ret)*(1+l18.ret) ) - 1
replace Mom18m13m  = -1*Mom18m13m 
label var Mom18m13m "Momentum-Reversal"
// SAVE
do "$pathCode/savepredictor" Mom18m13m