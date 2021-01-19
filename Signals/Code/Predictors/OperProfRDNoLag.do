* --------------
// DATA LOAD
use gvkey permno time_avail_m xrd revt cogs xsga at using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
gen tempXRD = xrd
replace tempXRD = 0 if mi(tempXRD)
gen OperProfRDNoLag = (revt - cogs - xsga + tempXRD)/at
label var OperProfRDNoLag "Operating profits to assets"
// SAVE
do "$pathCode/savepredictor" OperProfRDNoLag