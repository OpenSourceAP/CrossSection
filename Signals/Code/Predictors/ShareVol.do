* --------------
// DATA LOAD
use permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keepusing(shrout vol) nogenerate keep(match)
// SIGNAL CONSTRUCTION
gen ShareVol = (vol + l1.vol + l2.vol)/(3*shrout) // vol is in 100's, shrout is in 1000's
* original uses regressions, and ShareVol is right skewed
* so we remove the "uninformative" left mass
egen tempsort = fastxtile(ShareVol), by(time_avail_m) n(2)
replace ShareVol = . if tempsort == 1
label var ShareVol "Share Volume"
// SAVE
do "$pathCode/savepredictor" ShareVol