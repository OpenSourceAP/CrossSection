* --------------
// DATA LOAD
use permno time_avail_m emp using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen hire = (emp-l12.emp)/(.5*(emp + l12.emp))
replace hire = 0 if emp ==. | l12.emp ==.
replace hire = . if yofd(dofm(time_avail_m)) < 1965
label var hire "Employee growth"
// SAVE
do "$pathCode/savepredictor" hire