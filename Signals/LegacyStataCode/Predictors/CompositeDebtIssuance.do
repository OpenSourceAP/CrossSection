* CompositeDebtIssuance
* --------------

// DATA LOAD
use gvkey permno time_avail_m dltt dlc using "$pathDataIntermediate/m_aCompustat", clear

// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m

gen tempBD = dltt + dlc
gen CompositeDebtIssuance = log(tempBD/l60.tempBD)

label var CompositeDebtIssuance "Composite Debt Issuance"

// SAVE
do "$pathCode/savepredictor" CompositeDebtIssuance