* --------------
// DATA LOAD
use permno time_avail_m dvc prstkc sstk using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c) 
// SIGNAL CONSTRUCTION
gen NetPayoutYield = (dvc + prstkc - sstk)/mve_c
label var NetPayoutYield "Net Payout Yield"
// SAVE
do "$pathCode/savepredictor" NetPayoutYield