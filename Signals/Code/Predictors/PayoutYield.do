* --------------
// DATA LOAD
use permno time_avail_m dvc prstkc pstkrv sstk sic ceq datadate using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c) 


// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen PayoutYield = (dvc + prstkc + pstkrv)/l6.mve_c // page 882
replace PayoutYield = . if PayoutYield <= 0 // critical

// FILTER
destring sic, replace
keep if (sic < 6000 | sic >= 7000) & ceq > 0 // OP p 5: each of these filters helps
sort permno time_avail_m
bysort permno: keep if _n >= 24

// SAVE
label var PayoutYield "Payout Yield"
do "$pathCode/savepredictor" PayoutYield


