* --------------
// DATA LOAD
use gvkey permno time_avail_m am txt pi am epspx ajex prcc_f using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
replace am = 0 if mi(am)
gen tempTaxOverEBT = txt/(pi + am)
gen tempEarn = epspx/ajex
gen ETR = ( tempTaxOverEBT - 1/3*(l12.tempTaxOverEBT + l24.tempTaxOverEBT + l36.tempTaxOverEBT))*((tempEarn - l12.tempEarn)/l.prcc_f)
label var ETR "Effective Tax Rate"
// SAVE
do "$pathCode/saveplacebo" ETR