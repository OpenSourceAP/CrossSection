* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear

// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
asrol ret, by(permno) window(time_avail_m 10) stat(mean) minimum(6) gen(Mom12mOffSeason) xf(focal)  // xf(focal) excludes STR, the most recent return
label var Mom12mOffSeason "Momentum without Seasonal Part"

// SAVE
do "$pathCode/savepredictor" Mom12mOffSeason
