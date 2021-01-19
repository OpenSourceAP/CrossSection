* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keepusing(vol) nogenerate keep(match)
// SIGNAL CONSTRUCTION
replace vol = . if vol <0
replace ret = 0 if mi(ret)
gen Mom6m = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)) - 1
bys permno (time_avail_m): asrol vol, gen(temp) window(time_avail_m 6) min(5) stat(mean)
egen tempVol = fastxtile(temp), by(time_avail_m) n(5)
gen MomVol = Mom6m if tempVol == 5
bys permno (time_avail_m): replace MomVol = . if _n < 24
drop temp*
label var MomVol "Momentum-Volume"
// SAVE
do "$pathCode/savepredictor" MomVol