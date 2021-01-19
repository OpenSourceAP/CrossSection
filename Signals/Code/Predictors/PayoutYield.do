// 2021 01 ac: 
// added sic and ceq filter, changed to deciles following tab 3b
* --------------
// DATA LOAD
use permno time_avail_m dvc prstkc pstkrv sic ceq datadate using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c) 

destring sic, replace
keep if (sic < 6000 | sic >= 7000) & ceq > 0 // OP p 5: each of these filters helps

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen PayoutYield = (dvc + prstkc + max(pstkrv,0))/l6.mve_c
replace PayoutYield = . if PayoutYield <= 0 // critical
label var PayoutYield "Payout Yield"


// SAVE
do "$pathCode/savepredictor" PayoutYield