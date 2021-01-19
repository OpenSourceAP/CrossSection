* --------------
// DATA LOAD
use permno time_avail_m ret retx using "$pathDataIntermediate/monthlyCRSP", clear
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen DivInd = ( (l11.ret > l11.retx) | (l2.ret > l2.retx) )
label var DivInd "Dividend Indicator"
// SAVE
do "$pathCode/savepredictor" DivInd