* --------------
// DATA LOAD
use gvkey permno time_avail_m ib oancf dp act che lct txp dlc using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen PctAcc = (ib-oancf)/abs(ib) 

replace PctAcc = (ib - oancf)/.01 if ib == 0
replace PctAcc = ( (act-l12.act) - (che-l12.che) - (  (lct-l12.lct)- ///
    (dlc-l12.dlc)-(txp-l12.txp)-dp ) )/abs(ib) if oancf ==.
replace PctAcc = (   (act-l12.act) - (che-l12.che) - (  (lct-l12.lct)- ///
    (dlc-l12.dlc)-(txp-l12.txp)-dp ) )/.01 if oancf == . & ib ==0

label var PctAcc "Percent Operating PctAcc"
// SAVE
do "$pathCode/savepredictor" PctAcc