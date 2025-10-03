* --------------
// DATA LOAD
use gvkey permno time_avail_m sstk prstkc at dv using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen NetEquityFinance = (sstk - prstkc - dv)/(.5*(at + l12.at))
replace NetEquityFinance = . if abs(NetEquityFinance) > 1
label var NetEquityFinance "Net Equity Finance"
// SAVE
do "$pathCode/savepredictor" NetEquityFinance