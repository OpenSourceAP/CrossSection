* --------------
// DATA LOAD
use permno time_avail_m dvc prstkc sstk sic ceq using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c) 

// SIGNAL CONSTRUCTION
gen NetPayoutYield = (dvc + prstkc - sstk)/l6.mve_c
drop if NetPayoutYield == 0

destring sic, replace
keep if (sic < 6000 | sic >= 7000) & ceq > 0 // OP p 5
sort permno time_avail_m
bysort permno: keep if _n >= 24


// SAVE
label var NetPayoutYield "Net Payout Yield"
do "$pathCode/savepredictor" NetPayoutYield


