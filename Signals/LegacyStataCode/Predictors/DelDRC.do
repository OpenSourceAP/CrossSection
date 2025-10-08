* --------------
// DATA LOAD
use gvkey permno time_avail_m drc at ceq sale sic using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
destring sic, replace
gen DelDRC = (drc - l12.drc)/(.5*(at + l12.at))
replace DelDRC = . if ceq <=0 | (drc == 0 & DelDRC == 0) | sale < 5 | (sic >=6000 & sic < 7000) // (drc == 0 & DelDRC == 0) sets almost all to missing
                                                                                                // fn 8 says that it removes only a few??? http://pbfea2005.rutgers.edu/20thFEA/AccountingPapers/Session3/Prakash%20and%20Sinha.pdf
label var DelDRC "Deferred Revenue"
// SAVE
do "$pathCode/savepredictor" DelDRC