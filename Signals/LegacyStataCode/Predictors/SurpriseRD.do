* --------------
// DATA LOAD
use gvkey permno time_avail_m xrd revt at using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen SurpriseRD = 1 if xrd/revt > 0 & xrd/at > 0 & xrd/l12.xrd > 1.05 & ///
    (xrd/at)/(l12.xrd/l12.at) > 1.05 & xrd !=. & l12.xrd !=.
    
replace SurpriseRD = 0 if SurpriseRD==. & (xrd !=. & l12.xrd !=.)
label var SurpriseRD "Unexpected R&D increase"
// SAVE
do "$pathCode/savepredictor" SurpriseRD