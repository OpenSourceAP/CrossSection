* --------------
// DATA LOAD
use permno time_avail_m vol prc shrout using "$pathDataIntermediate/monthlyCRSP", clear
// SIGNAL CONSTRUCTION
gen mve_c =  (shrout * abs(prc))
gen temp = vol*abs(prc)
bys permno: asrol temp, gen(tempMean) stat(mean) window(time_avail_m 12) min(10)
gen VolMkt = tempMean/mve_c
label var VolMkt "Volume to market equity"
// SAVE
do "$pathCode/savepredictor" VolMkt
