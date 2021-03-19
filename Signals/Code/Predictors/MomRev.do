* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
gen Mom6m = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)) - 1
gen Mom36m = (   (1+l13.ret)*(1+l14.ret)*(1+l15.ret)*(1+l16.ret)*(1+l17.ret)*(1+l18.ret)   * ///
    (1+l19.ret)*(1+l20.ret)*(1+l21.ret)*(1+l22.ret)*(1+l23.ret)*(1+l24.ret)* ///
    (1+l25.ret)*(1+l26.ret)*(1+l27.ret)*(1+l28.ret)*(1+l29.ret)*(1+l30.ret)     * ///
    (1+l31.ret)*(1+l32.ret)*(1+l33.ret)*(1+l34.ret)*(1+l35.ret)*(1+l36.ret)  ) - 1
    
egen tempMom6  = fastxtile(Mom6m), by(time_avail_m) n(5)
egen tempMom36 = fastxtile(Mom36m), by(time_avail_m) n(5)
gen MomRev = 1 if tempMom6 == 5 & tempMom36 == 1
replace MomRev = 0 if tempMom6 == 1 & tempMom36 == 5
label var MomRev "Momentum and LT Reversal"
// SAVE
do "$pathCode/savepredictor" MomRev