* AccrualQuality, AccrualQualityJune
* --------------

// DATA LOAD
use gvkey permno time_avail_m datadate fyear ib act che lct dlc dp at sale sic ppegt using "$pathDataIntermediate/a_aCompustat", clear

// SIGNAL CONSTRUCTION
xtset gvkey fyear

gen tempAccruals = ( (act - l.act) - (che - l.che) - ( (lct - l.lct) - ///
	(dlc - l.dlc)  ) - dp) / ( (at + l.at)/2)
gen tempCAcc = tempAccruals + dp/( (at + l.at)/2)	
gen tempRev = sale/( (at + l.at)/2)
gen tempDelRev = tempRev - l.tempRev
gen tempPPE = ppegt/( (at + l.at)/2)
gen tempCFO = ib/( (at + l.at)/2) - tempAccruals

* Run regressions for each year and industry
destring sic, replace
ffind sic, newvar(FF48) type(48)
gen tempResid = .
levelsof fyear
foreach y of numlist `r(levels)' {
	foreach ind of numlist 1/48 {
		cap drop tempU
		cap reg tempCAcc l(-1/1).tempCFO tempDelRev tempPPE if fyear == `y' & FF48 == `ind'
		cap predict tempU if e(sample), resid
		cap replace tempResid = tempU if e(sample)
	}
}
bys fyear FF48: replace tempResid = . if _N < 20  // At least 20 observations per year and industry required

* Rolling standard deviation
xtset gvkey fyear
foreach n of numlist 1/4 {
	gen tempResid`n' = l`n'.tempResid
}

egen AQ = rowsd(tempResid*)
egen tempN = rowmiss(tempResid*)	
replace AQ = . if tempN > 1
mdesc AQ
cap drop temp* FF48

gen AccrualQuality = l.AQ  // Construction uses one year ahead operating cash flow so need to lag

label var AccrualQuality "Accrual Quality"

* Expand to monthly
gen temp = 12
expand temp
drop temp

gen tempTime = time_avail_m
bysort gvkey tempTime: replace time_avail_m = time_avail_m + _n - 1 

drop tempTime
bysort permno time_avail_m (datadate): keep if _n == _N 

* Accrual quality June
gen AccrualQualityJune = AccrualQuality if month(dofm(time_avail_m)) == 6
bys permno (time_avail_m): replace AccrualQualityJune = AccrualQualityJune[_n-1] if mi(AccrualQualityJune)

label var AccrualQualityJune "Accrual Quality (June version)"

// SAVE
do "$pathCode/saveplacebo" AccrualQuality
do "$pathCode/saveplacebo" AccrualQualityJune