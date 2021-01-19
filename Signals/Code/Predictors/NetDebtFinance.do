* --------------
// DATA LOAD
use gvkey permno time_avail_m dlcch dltis dltr at using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
replace dlcch = 0 if mi(dlcch)
gen NetDebtFinance = (dltis - dltr - dlcch)/(.5*(at + l12.at))
replace NetDebtFinance = . if abs(NetDebtFinance) > 1
label var NetDebtFinance "NetDebtFinance"
// SAVE
do "$pathCode/savepredictor" NetDebtFinance