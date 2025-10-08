* --------------
// DATA LOAD
use gvkey permno time_avail_m ppegt invt at using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen tempPPE = ppegt - l12.ppegt
gen tempInv = invt  - l12.invt 
gen InvestPPEInv = (tempPPE + tempInv)/l12.at
label var InvestPPEInv "PPE and inventory changes to assets"
// SAVE
do "$pathCode/savepredictor" InvestPPEInv