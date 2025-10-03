* Accruals
* --------------

// DATA LOAD
use gvkey permno time_avail_m txp act che lct dlc at dp using "$pathDataIntermediate/m_aCompustat", clear

// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m

gen tempTXP = txp
replace tempTXP = 0 if mi(txp)

* see eq 1, p 6 of Sloan 1996	
gen Accruals = ( (act - l12.act) - (che - l12.che) ///
	- ( (lct - l12.lct) - (dlc - l12.dlc) - (tempTXP - l12.tempTXP) ) ///
	- dp ) / ( (at + l12.at)/2)
	
drop temp*
label var Accruals "Accruals"

// SAVE
do "$pathCode/savepredictor" Accruals


