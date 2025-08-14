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
* CHECKPOINT 1: After creating Mom6m and Mom36m
list permno time_avail_m Mom6m Mom36m if permno == 10028 & time_avail_m == tm(2007m10), noobs
    
egen tempMom6  = fastxtile(Mom6m), by(time_avail_m) n(5)
* CHECKPOINT 2: After fastxtile for Mom6m
list permno time_avail_m Mom6m tempMom6 if permno == 10028 & time_avail_m == tm(2007m10), noobs
egen tempMom36 = fastxtile(Mom36m), by(time_avail_m) n(5)
* CHECKPOINT 3: After fastxtile for Mom36m
list permno time_avail_m Mom36m tempMom36 if permno == 10028 & time_avail_m == tm(2007m10), noobs
gen MomRev = 1 if tempMom6 == 5 & tempMom36 == 1
replace MomRev = 0 if tempMom6 == 1 & tempMom36 == 5
* CHECKPOINT 4: When creating MomRev conditions
list permno time_avail_m tempMom6 tempMom36 MomRev if permno == 10028 & time_avail_m == tm(2007m10), noobs
label var MomRev "Momentum and LT Reversal"
// SAVE
do "$pathCode/savepredictor" MomRev