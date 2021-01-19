* --------------
// DATA LOAD
use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
drop if mi(gvkey)
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(match) nogenerate keepusing(shrout)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/monthlyShortInterest", keep(match) nogenerate keepusing(shortint)
// SIGNAL CONSTRUCTION
gen ShortInterest = shortint/shrout
label var ShortInterest "Short interest"
// SAVE
do "$pathCode/savepredictor" ShortInterest