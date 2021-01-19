* AbnormalAccruals, AbnormalAccrualsPercent
* --------------


// DATA LOAD
use gvkey permno time_avail_m fyear datadate at oancf fopt act che lct dlc ib sale ppegt ni sic  using "$pathDataIntermediate/a_aCompustat", clear

// SIGNAL CONSTRUCTION
xtset gvkey fyear

// Compute abnormal accruals for Xie (2001)
gen tempCFO = oancf
replace tempCFO = fopt - (act - l.act) + (che - l.che) + (lct - l.lct) - (dlc - l.dlc) if mi(tempCFO)
gen tempAccruals = (ib - tempCFO) / ((at + l.at)/2)
gen tempInvTA = 1/((at + l.at)/2)
gen tempDelRev = (sale - l.sale)/( (at + l.at)/2)
gen tempPPE = ppegt/( (at + l.at)/2)

* Run regressions for each year and industry
destring sic, replace
ffind sic, newvar(FF48) type(48)  // Xie uses 2 digit sic industry instead
gen tempResid = .
levelsof fyear
foreach y of numlist `r(levels)' {
	foreach ind of numlist 1/48 {
		cap drop tempU
		cap reg tempAccruals tempInvTA tempDelRev tempPPE if fyear == `y' & FF48 == `ind'
		cap predict tempU if e(sample), resid
		cap replace tempResid = tempU if e(sample)
	}
}

rename tempResid AbnormalAccruals
cap drop temp* FF48

label var AbnormalAccruals "Abnormal Accruals"

* Abnormal Accruals Percent
gen AbnormalAccrualsPercent = AbnormalAccruals*l.at/abs(ni)
label var AbnormalAccrualsPercent "Abnormal Accruals (Percent)"

* Expand to monthly
gen temp = 12
expand temp
drop temp

gen tempTime = time_avail_m
bysort gvkey tempTime: replace time_avail_m = time_avail_m + _n - 1 

drop tempTime
bysort gvkey time_avail_m (datadate): keep if _n == _N 
bysort permno time_avail_m (datadate): keep if _n == _N 

// SAVE 
do "$pathCode/savepredictor" AbnormalAccruals
do "$pathCode/savepredictor" AbnormalAccrualsPercent