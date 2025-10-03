* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
gen LRreversal = (   (1+l13.ret)*(1+l14.ret)*(1+l15.ret)*(1+l16.ret)*(1+l17.ret)*(1+l18.ret)   * ///
    (1+l19.ret)*(1+l20.ret)*(1+l21.ret)*(1+l22.ret)*(1+l23.ret)*(1+l24.ret)* ///
    (1+l25.ret)*(1+l26.ret)*(1+l27.ret)*(1+l28.ret)*(1+l29.ret)*(1+l30.ret)     * ///
    (1+l31.ret)*(1+l32.ret)*(1+l33.ret)*(1+l34.ret)*(1+l35.ret)*(1+l36.ret)  ) - 1
    
label var LRreversal "LT reversal"
// SAVE
do "$pathCode/savepredictor" LRreversal