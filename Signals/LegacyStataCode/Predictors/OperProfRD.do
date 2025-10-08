* OperProfRD
* --------------
* some confusion about lagging assets or not
* OP 2016 JFE seems to lag assets, but 2015 JFE does not
* Yet no lag implies results much closer to OP

// DATA LOAD
use permno gvkey time_avail_m exchcd sicCRSP mve_c shrcd using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", nogenerate keep(master match) ///
	keepusing(gvkey permno time_avail_m xrd revt cogs xsga at ceq)

// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
gen tempXRD = xrd
replace tempXRD = 0 if mi(tempXRD)
gen OperProfRD = (revt - cogs - xsga + tempXRD)/at
label var OperProfRD "Operating profits to assets"
drop if shrcd > 11 | mi(mve_c) | mi(ceq) | mi(at) | (sicCRSP >= 6000 & sicCRSP < 7000)

// SAVE
do "$pathCode/savepredictor" OperProfRD

