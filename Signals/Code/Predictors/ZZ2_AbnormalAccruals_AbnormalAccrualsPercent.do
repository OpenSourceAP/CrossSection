* AbnormalAccruals, AbnormalAccrualsPercent
* --------------


// DATA LOAD
use gvkey permno time_avail_m fyear datadate at oancf fopt act che lct dlc ib sale ppegt ni sic  using "$pathDataIntermediate/a_aCompustat", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(master match) keepusing(exchcd)

// SIGNAL CONSTRUCTION
xtset gvkey fyear

// Compute abnormal accruals for Xie (2001)
gen tempCFO = oancf
replace tempCFO = fopt - (act - l.act) + (che - l.che) + (lct - l.lct) - (dlc - l.dlc) if mi(tempCFO)
gen tempAccruals = (ib - tempCFO) / l.at
gen tempInvTA = 1/l.at
gen tempDelRev = (sale - l.sale)/l.at
gen tempPPE = ppegt/l.at

* CHECKPOINT 1: Check accruals calculation for problem observations before winsorization
list permno gvkey fyear tempCFO tempAccruals tempInvTA tempDelRev tempPPE if permno == 79702 & fyear >= 2017 & fyear <= 2018

sort fyear
winsor2 temp*, replace cuts(0.1 99.9) trim by(fyear)  // p 360 (approx)

* CHECKPOINT 2: Check accruals after winsorization for problem observations
list permno gvkey fyear tempCFO tempAccruals tempInvTA tempDelRev tempPPE if permno == 79702 & fyear >= 2017 & fyear <= 2018

// * Run regressions for each year and industry
destring sic, replace
gen sic2 = floor(sic/100)

* CHECKPOINT 3: Check SIC2 industry codes for problem observations  
list permno gvkey fyear sic sic2 if permno == 79702 & fyear >= 2017 & fyear <= 2018

bys fyear sic2: asreg tempAccruals tempInvTA tempDelRev tempPPE , fitted

* CHECKPOINT 4: Check regression results for problem observations
list permno gvkey fyear _Nobs _fitted _residuals if permno == 79702 & fyear >= 2017 & fyear <= 2018

drop if _Nobs < 6 // p 360
drop if exchcd == 3 & fyear < 1982

* CHECKPOINT 5: Check residuals after filtering for problem observations
list permno gvkey fyear _residuals if permno == 79702 & fyear >= 2017 & fyear <= 2018

rename _residuals AbnormalAccruals
drop _* temp* 

* drop a few duplicates
sort permno fyear
by permno fyear: keep if _n == 1

label var AbnormalAccruals "Abnormal Accruals"

* Abnormal Accruals Percent
xtset permno fyear
gen AbnormalAccrualsPercent = AbnormalAccruals*l.at/abs(ni)
label var AbnormalAccrualsPercent "Abnormal Accruals (Percent)"

* CHECKPOINT 6: Check final AbnormalAccruals values before monthly expansion
list permno gvkey fyear time_avail_m AbnormalAccruals if permno == 79702 & fyear >= 2017 & fyear <= 2018

* Expand to monthly
gen temp = 12
expand temp
drop temp

gen tempTime = time_avail_m
bysort gvkey tempTime: replace time_avail_m = time_avail_m + _n - 1 

drop tempTime
bysort gvkey time_avail_m (datadate): keep if _n == _N 
bysort permno time_avail_m (datadate): keep if _n == _N

* CHECKPOINT 7: Check monthly expansion for problem observations
list permno time_avail_m AbnormalAccruals if permno == 79702 & time_avail_m >= tm(2017m12) & time_avail_m <= tm(2018m12), noobs 

// SAVE 
do "$pathCode/savepredictor" AbnormalAccruals
do "$pathCode/saveplacebo" AbnormalAccrualsPercent


