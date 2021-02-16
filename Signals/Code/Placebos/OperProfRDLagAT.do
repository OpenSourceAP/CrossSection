* --------------
// DATA LOAD
use gvkey permno time_avail_m xrd revt cogs xsga at using "$pathDataIntermediate/m_aCompustat", clear

// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen tempXRD = xrd
replace tempXRD = 0 if mi(tempXRD)
gen OperProfRDLagAT = (revt - cogs - xsga + tempXRD)/l12.at
label var OperProfRDLagAT "Operating profits to lagged assets"

// SAVE
do "$pathCode/saveplacebo" OperProfRDLagAT
