* --------------
// DATA LOAD
use gvkey permno time_avail_m ebit nopi ceq lt che using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
gen roic = (ebit - nopi)/(ceq + lt - che)
label var roic "Return on invested capital"
// SAVE
do "$pathCode/saveplacebo" roic