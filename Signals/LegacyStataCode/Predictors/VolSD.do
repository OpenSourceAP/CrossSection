* --------------
// DATA LOAD
use permno time_avail_m vol using "$pathDataIntermediate/monthlyCRSP", clear
// SIGNAL CONSTRUCTION
bys permno: asrol vol, gen(VolSD) stat(sd) window(time_avail_m 36) min(24)
label var VolSD "Volume variance"
// SAVE
do "$pathCode/savepredictor" VolSD