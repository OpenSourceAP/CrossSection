* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
asrol ret, by(permno) window(time_avail_m 10) stat(mean) minimum(6) gen(MomSeasAlt1n) xf(focal)  // xf(focal) excludes STR, the most recent return
label var MomSeasAlt1n "Non-seasonal return (year 1)"
// SAVE
do "$pathCode/savepredictor" MomSeasAlt1n