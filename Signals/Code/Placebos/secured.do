* --------------
// DATA LOAD
use permno time_avail_m dm dltt dlc using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
gen secured = dm/(dltt+dlc)
replace secured = 0 if dltt ==. | dltt ==0 | dlc == .
label var secured "Secured debt over liabilities"

// SAVE
do "$pathCode/saveplacebo" secured