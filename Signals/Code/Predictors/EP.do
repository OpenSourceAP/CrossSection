* --------------
// DATA LOAD
use gvkey permno time_avail_m ib using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(mve_c)
// SIGNAL CONSTRUCTION
* original paper uses Dec 31 obs for ib and mve_c, while our 
* mve_c gets updated monthly.  Thus, we lag mve_c 6 months
* to try to get at the spirit of the original paper.  
* this lag helps a lot, as it seems to remove momentum effects.
* excluding EP < 0 and using the original sample (not MP's) helps too
xtset permno time_avail_m
gen EP = ib/l6.mve_c
replace EP  = . if EP < 0
label var EP "Earnings-to-price ratio"
// SAVE
do "$pathCode/savepredictor" EP